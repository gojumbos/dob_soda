import logging
from datetime import datetime, timedelta

import flask

import supa
from main import main
import em

import html

from flask import Flask, request, jsonify, after_this_request, render_template
from flask import send_from_directory, make_response

import os


from random import randint
import soda

import cron

""" New 6.19 """
# api routes
import routes
#
# frontend_folder = os.path.join(os.getcwd(),"..","frontend")
# dist_folder = os.path.join(frontend_folder,"dist")


class AppController:
    def __init__(self, dev_server=False,
                 supa_wrapper=None):
        self.dev_server = dev_server
        self.app_object = Flask(__name__,  # 7/9
                                )
        self.all_users = {}
        self.supa_wrapper = supa_wrapper

        self.no_fly_list = {}  # cookies

    def add_to_no_fly_list(self, token=""):
        self.no_fly_list[token] = None

    def is_on_no_fly_list(self, token=""):
        return token in self.no_fly_list

    def add_logged_in_user(self, email: str, access_token):
        """ replace if existing """
        if email not in self.all_users:
            self.all_users[email] = access_token
            # self.app_object.logger.info(str(email), "Added")
        else:
            self.app_object.logger.warning(f'MULTIPLE SESSIONS FOR {email}')
            self.all_users[email] = access_token

    def remove_logged_in_user(self, email: str):
        assert type(self.supa_wrapper) is supa.SupaClientWrapper
        self.supa_wrapper.sb_client.auth.sign_out()
        self.all_users.pop(email)

""" END APP CLASS """
sw = supa.SupaClientWrapper()
app_controller = AppController(supa_wrapper=sw)
app = app_controller.app_object
logger = logging.getLogger('logger')


# @app.route('/stat', methods=['GET'])
# def home():  # put application's code here
#     # token = request.cookies['cookie1']
#     # if token:
#     #     if app_controller.is_on_no_fly_list(token):
#     #         return "", 500
#     return flask.render_template('index.html')



@app.route('/', methods=['GET'])
def home():  # put application's code here
    # token = request.cookies['cookie1']
    # if token:
    #     if app_controller.is_on_no_fly_list(token):
    #         return "", 500
    """"""
    """ js """
    js_path = os.path.join(app.static_folder, 'js', 'main.js')
    with open(js_path, 'r') as js_file:
        js_content = js_file.read()
    """ css """
    css_path = os.path.join(app.static_folder, 'css', 'styles.css')
    with open(css_path, 'r') as css_file:
        css_content = css_file.read()
    return flask.render_template('index.html',
                                 js_content=js_content,
                                 css_content=css_content)

@app.route('/api', methods=['GET'])
def api_home():  # put application's code here
    # token = request.cookies['cookie1']
    # if token:
    #     if app_controller.is_on_no_fly_list(token):
    #         return "", 500
    return flask.render_template('index.html')


# soda
@app.route('/api/soda_get_update', methods=['GET'])
def soda_check_update():
    """ api endpoint for cron job
    basic pass phrase check, non-security viable
    7-16-24
    """
    data = request.get_json()
    phrase = request.headers.get('Authorization')
    if phrase != 'icecream999':
        return jsonify({'message': 'Request failed'}), 400
    r = cron.cron_run()
    return "", 200
    # """ **** FINISH


@app.route('/api/delete_item', methods=['POST'])
def delete_item():
    """ given type and id, drop from table """
    data = request.get_json()
    token = request.cookies['cookie1']
    email = data.get('email')  # error
    item_type = data.get('item_type')
    identifier = data.get('identifier')
    col = data.get('col')

    tables = {'building': 'buildings_tracked',
              'entity': 'entities_tracked',
              'filing': 'filings_tracked'
              }

    app_ = app
    supa_wrapper = app_controller.supa_wrapper
    text, code = supa_wrapper.supa_delete_item(access_token=token,
                                               app=app_,
                                               table=tables[item_type],
                                               col=col,
                                               identifier=identifier
                                        )
    if code == 200:
        # response = jsonify(text), 200
        # app_c.logger.info(response)
        # html = prepare_data_table(input_text=text)
        response = "success", 200
        return response
    else:
        response = jsonify({'message': 'Request failed'}), 400
        app.logger.info(response)
    return response


@app.route('/api/trying', methods=['POST'])
def captcha():
    # token = request.cookies['cookie1']
    msg = "", 500
    response = make_response(msg)
    r_str = str(randint(1, 10000)) + "qyOTwQvxuZBX"
    response.set_cookie('cookie1', r_str)
    app_controller.add_to_no_fly_list(token=r_str)
    return "", 500


@app.route('/test_email')
def test_email():
    """
    send test email
    """
    emailer = em.EmailInterface()
    emailer.test_send_email()
    return 'done debug'


@app.route('/api/login', methods=['POST'])
def login():
    """ given request with creds from browser,
    attempt supabase login
    and add session to existing sessions
    >> no duplicate sessions?
    """
    data = request.get_json()
    email = data.get('email')  # error
    password = data.get('password')
    # token = request.cookies['cookie1']
    # if email in app_controller.all_users:
    #     if app_controller.all_users[email] == 'cookie1':

    app_copy = app

    supa_wrapper = app_controller.supa_wrapper

    # supabase.auth.set_session(access_token=access_token, refresh_token=refresh_token)

    token, code = supa_wrapper.supa_login(email=email, password=password,
                                          app=app_copy)
    """ INSECURE: bypass RLS """
    # r = supa_wrapper.service_check_credentials(email=email, password=password,
    #                             app=app)

    if code == 200:
        msg = jsonify({'message': 'Login successful'}), 200
        response = make_response(msg)
        response.set_cookie('cookie1', token)
        app_controller.add_logged_in_user(email=email, access_token=token)
    else:
        response = jsonify({'message': 'Login failed'}), 401

    return response


@app.route('/api/get_user_data', methods=['POST'])
def get_user_data():

    data = request.get_json()
    token = request.cookies['cookie1']
    email = data.get('email')  # error
    # apc = AppController()

    # local_token = app_controller.all_users[email]

    app_c = app
    supa_wrapper = app_controller.supa_wrapper
    text, code = supa_wrapper.get_items(access_token=token,
                                        app=app_c,
                                        limit=None,
                                        table='job_apps_yesterday'
                                        )

    # supabase.auth.set_session(access_token=access_token, refresh_token=refresh_token)

    html = prepare_data_table(input_text=text)

    if code == 200:
        # response = jsonify(html), 200
        response = str(html), 200
        # app_c.logger.info(response)
        return response
    else:
        response = jsonify({'message': 'Request failed'}), 401
        app_c.logger.info(response)
    return response


@app.route('/api/get_user_tracked_entities', methods=['POST'])
def get_user_tracked_entities():
    """ check: assert email? """

    data = request.get_json()
    token = request.cookies['cookie1']
    email = data.get('email')  # error
    app_ = app
    supa_wrapper = app_controller.supa_wrapper
    text, code = supa_wrapper.get_items(access_token=token,
                                        app=app_,
                                        table='entities_tracked',
                                        limit=None)
    if code == 200:
        # response = jsonify(text), 200
        # app_c.logger.info(response)
        html = prepare_data_table(input_text=text)
        response = str(html), 200
        return response
    else:
        response = jsonify({'message': 'Request failed'}), 400
        app.logger.info(response)
    return response


@app.route('/api/submit_new_entity', methods=['POST'])
def get_new_entity_tracked():
    data = request.get_json()
    token = request.cookies['cookie1']
    email = data.get('email')  # error

    fields = ['entity_type', 'applicant_first_name', 'applicant_last_name',
              'owner_s_business_name',
              'applicant_license']

    d = {}
    for f in fields:
        content = data.get(f)
        # ignore empty fields
        if not content == "":
            d[f] = content
            # sanitize
            # need spec
            if not content.isalnum():
                return jsonify({'message': 'Bad input characters'}), 400

    app_ = app
    supa_wrapper = app_controller.supa_wrapper
    text, code = supa_wrapper.add_item_to_table(access_token=token,
                                                app=app_,
                                                data_dict=d,
                                                )
    if code == 200:
        response = jsonify(text), 200
        app_.logger.info(response)
        return response
    else:
        response = jsonify({'message': 'Request failed'}), 401
        app.logger.info(response)
    return response


# -building
@app.route('/api/submit_new_building', methods=['POST'])
def get_new_building_tracked():
    data = request.get_json()
    token = request.cookies['cookie1']
    email = data.get('email')  # error

    content = data.get('bin')
    if not content.isalnum() or content == "":
        return jsonify({'message': 'Bad input characters'}), 400

    d = {"bin": content}

    app_ = app
    supa_wrapper = app_controller.supa_wrapper
    text, code = supa_wrapper.add_item_to_table(access_token=token,
                                                app=app_,
                                                data_dict=d,
                                                table_name="buildings_tracked")
    if code == 200:
        response = jsonify(text), 200
        app_.logger.info(response)
        return response
    else:
        response = jsonify({'message': 'Request failed'}), 401
        app.logger.info(response)
    return response


@app.route('/api/get_user_tracked_buildings', methods=['POST'])
def get_user_tracked_buildings():
    """ check: assert email? """

    data = request.get_json()
    token = request.cookies['cookie1']
    email = data.get('email')  # error
    app_ = app
    supa_wrapper = app_controller.supa_wrapper
    text, code = supa_wrapper.get_items(access_token=token,
                                        app=app_,
                                        limit=None,
                                        table="buildings_tracked"
                                        )
    if code == 200:
        # response = jsonify(text), 200
        # app_c.logger.info(response)
        html = prepare_data_table(input_text=text)
        response = str(html), 200
        return response
    else:
        response = jsonify({'message': 'Request failed'}), 400
        app.logger.info(response)
    return response



def prepare_data_table(input_text=""):
    """"""
    html = ""
    emi = em.EmailInterface(dummy=True)
    html = emi.template_table_js(raw_data=input_text,
                                 )

    return html



""" END create app"""

#
# """ TEST !!  remove me """
# test = False
# # test = True
# if test:
#     print("TEST")
#     app = app_controller.app_object
#     sw = supa.SupaClientWrapper()
#
#     acc_token, r = sw.supa_login(email="holden@hrgcap.com", password='hrg')
#     print(acc_token)
#
#     text, code = sw.get_entities(access_token=acc_token,
#                                            app=app,
#                                            limit=None)
#
#     # data = sw.get_dob_data(access_token=acc_token, app=app)
#
#     # text, code = sw.get_dob_data(access_token=acc_token,
#     #                                        app=app,
#     #                                        limit=10
#     #                                        )
#
#
#     # supabase.auth.set_session(access_token=access_token, refresh_token=refresh_token)
#
#     html = prepare_data_table(input_text=text)
#     print(html)
#
#
# # if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9000)