import logging
import re
from datetime import datetime, timedelta

import flask
from dotenv import load_dotenv

import supa
import em

import html

from flask import Flask, request, jsonify, after_this_request, render_template
from flask import send_from_directory, make_response

import os


from random import randint
import soda

import cron
import constants

import manual

class AppController:
    def __init__(self, dev_server=False,
                 supa_wrapper=None):
        self.dev_server = dev_server
        self.app_object = Flask(__name__,  # 7/9
                                )
        self.all_users = {}  # 8/22 : token -> email
        self.supa_wrapper = supa_wrapper

        self.no_fly_list = {}  # cookies
        self.curr_env = None  # indicator
        self.CURR_ENV_LINK_LIT = None

    def add_to_no_fly_list(self, token=""):
        self.no_fly_list[token] = None

    def is_on_no_fly_list(self, token=""):
        return token in self.no_fly_list

    def has_token(self, token=""):
        # jwt exists
        return token in self.all_users

    def add_logged_in_user(self, email: str, access_token):
        """ replace if existing
        8/22
         """
        # if email not in self.all_users:
        #     self.all_users[email] = access_token
        # else:
        #     self.app_object.logger.warning(f'MULTIPLE SESSIONS FOR {email}')
        #     self.all_users[email] = access_token

        if access_token not in self.all_users:
            self.all_users[access_token] = email
        else:
            self.app_object.logger.warning(f'MULTIPLE SESSIONS FOR {email}')
            self.all_users[access_token] = email

    def remove_logged_in_user(self, token: str):
        assert type(self.supa_wrapper) is supa.SupaClientWrapper
        self.supa_wrapper.sb_client.auth.sign_out()
        self.all_users.pop(token)


    def  get_logged_in_email_from_token(self, token: str):
        return self.all_users.get(token) if token in self.all_users else ""


""" END APP CLASS """
sw = supa.SupaClientWrapper()
app_controller = AppController(supa_wrapper=sw)
app = app_controller.app_object
logger = logging.getLogger('logger')
load_dotenv()

@app.route('/', methods=['GET'])
def landing_page():
    """ remove 'api' from home links """
    app_controller.curr_env = os.getenv('CURR_ENV')  # dev/prod
    app_controller.CURR_ENV_LINK_LIT = constants.HOME_URL_LIT_SEL[app_controller.curr_env]
    fav_link = app_controller.CURR_ENV_LINK_LIT.replace("api", "") + "static/tiles_1.jpeg"

    home_link = app_controller.CURR_ENV_LINK_LIT.replace("api", "") + "home"

    return render_template('landing.html',
                           home_link=home_link,
                           fav_link=fav_link,)

# @app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    # token = request.cookies['cookie1']
    # if token:
    #     if app_controller.is_on_no_fly_list(token):
    #         return "", 500
    """ """
    # token = request.cookies['cookie1'] if 'cookie1' in request.cookies else None
    # if token:
    #     if app_controller.has_token(token=token):
    #         """ double check; if logged in, return data table """
    #         if check_log_in(access_token=token,):
    #             # call API endpoint *function* directly
    #             return get_user_data(active=True, token=token)

    """"""
    app_controller.curr_env = os.getenv('CURR_ENV')  # dev/prod
    app_controller.CURR_ENV_LINK_LIT = constants.HOME_URL_LIT_SEL[app_controller.curr_env]
    """ js """
    js_path = os.path.join(app.static_folder, 'js', 'main.js')
    with open(js_path, 'r') as js_file:
        js_content = js_file.read()
        if app_controller.curr_env == 'dev':
            js_content = js_content.replace('999_', constants.HOME_URL_DEV)
        else:
            js_content = js_content.replace('999_', constants.HOME_URL_PROD)

    """ css """
    css_path = os.path.join(app.static_folder, 'css', 'styles.css')
    with open(css_path, 'r') as css_file:
        css_content = css_file.read()

    # 8/15
    link = app_controller.CURR_ENV_LINK_LIT.replace("api", "") + "static/favicon.ico"

    return flask.render_template('index.html',
                                 js_content=js_content,
                                 css_content=css_content,
                                 fav_link=link
                                 )


def check_log_in(access_token: str):
    """ check if request contains cookies from an
    existing user session. return True if so, else False
    """
    app_ = app
    supa_wrapper = app_controller.supa_wrapper
    # delete me
    text, code = supa_wrapper.check_user_session(access_token=access_token,
                                                 app=app_
                                               )
    app_controller.app_object.logger.warning("checklogin", code, text)
    return True if code == 200 else False

@app.route('/api/soda_display_json', methods=['GET'])
def soda_display_json():
    """ manual endpoint for debugging
    returns raw json output from request
    """
    # data = request.get_json()
    r, data = cron.cron_run(testing=True, time_diff=1, write=False)
    from manual import raw_json
    return raw_json(data)


@app.route('/api/get_favicon')  # name change?
def favicon():
    app.logger.error('FAVICON__')
    return app.send_static_file('favicon.ico')


# soda
@app.route('/api/soda_get_update', methods=['GET'])
def soda_check_update():
    """ api endpoint for cron job
    basic pass phrase check, non-security viable
    7-16-24
    """
    # data = request.get_json()
    phrase = request.headers.get('Authorization')
    if phrase != os.getenv('CRON_KEY'):
        return jsonify({'message': 'Request failed'}), 400
    data = cron.cron_run()
    return data, 200



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
    # if not active:  # fresh log in from client
    data = request.get_json()
    token = request.cookies['cookie1']
    email = data.get('email')  # error
    # else:
    #     token = token
    #     email = app_controller.get_logged_in_email_from_token(token=token)

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
        response = str(html), 200
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
        if (not content == "" or content):
            clean = re.sub('[^A-Za-z0-9]+', '', content)
            d[f] = clean
            # sanitize
            # need spec
            # if not content.isalnum():
                # return jsonify({'message': 'Bad input characters'}), 400
                # return jsonify({'message': content}), 400


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


def prepare_data_table(input_text="",):
    """
    user data = all JAY data, basic
    entity
    building
    """
    html = ""
    emi = em.EmailInterface(dummy=True)
    html = emi.template_table_js(raw_data=input_text,
                                 )
    return html



""" END create app"""
