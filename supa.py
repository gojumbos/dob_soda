

import os
from typing import List

import requests
from supabase import create_client, Client
from dotenv import load_dotenv

import time


class SupaClientWrapper:
    def __init__(self, service=True):
        load_dotenv()
        self.url: str = os.environ.get("SUPABASE_URL")
        if service:
            self.key: str = os.environ.get("DANGER_SUPABASE_SERVICE")  # service role
            self.sb_client: Client = create_client(self.url, self.key)
        else:
            # self.url: str = os.environ.get("SUPABASE_URL")
            self.key = os.environ.get("SUPABASE_KEY")
            return
        return

    def overwrite_yday_table(self, table_name: str, rows: List):
        # response = supabase.table('all_users').select("email_address").execute()

        data, count = ((self.sb_client.table(table_name=table_name)
                       .insert({"id": 1, "name": "Denmark"}))
                       .execute())
        return

    def read_table(self, table_name='job_apps_yesterday',
                   col_names='*',
                   limit=None):
        """ DEFAULT: read JAY table, all columns """
        # 'job_filing_number'
        cols = col_names  # a str
        response = self.sb_client.table(table_name=table_name).select(cols).execute()
        # rows = [list(d.values())[0] for d in response.data]  # list of dicts
        data = response.data
        if limit:
            data = data[:limit]
        return data

    def service_check_credentials(self, email: str, password: str,
                                  app=None):
        """ 6/20 - insecure """
        response = (self.sb_client.table(table_name='all_users')
                    .select('email, password')
                    .eq('all_users.email', email)
                    .execute())


        return

    def supa_login(self, email: str, password: str,
                   app=None):
        # app.logger.info(email, "EMAIL ")
        # app.logger.info(password, "password str ")
        try:
            data = self.sb_client.auth.sign_in_with_password({"email": email,
                                                              "password": password})
            # app.logger.info(data)
            session = data.session
            self.sb_client.postgrest.auth(token=session.access_token)
            access_token = session.access_token
            return access_token, 200
        except Exception as e:
            app.logger.error(e)
            return None, 401


    def get_all_email_addresses(self,):
        """ log in as admin, get all email addresses """
        emails = []
        response = self.sb_client.table('all_users').select("email_address").execute()
        emails = [list(d.values())[0] for d in response.data]  # list of dicts
        return emails

    """ 6/27 """
    def supa_delete_item(self, access_token=None, app=None,
                         table=None, identifier=None, col=None):
        """ delete item from table given col, identifier """
        try:
            self.sb_client.postgrest.auth(token=access_token)

            response = (self.sb_client.table(table)
                        .delete()
                        .eq(col, identifier)
                        .execute())

            return response, 200

        except Exception as e:
            app.logger.error(e)
            return "Bad request, or identifying information was not found", 401

    """ 6/21 """
    def get_items(self, access_token=None, app=None, limit=None,
                  table='entities_tracked'):
        try:
            self.sb_client.postgrest.auth(token=access_token)

            response = (self.sb_client.table(table)
                        .select("*").execute())

            if limit:
                data = response.data[:limit]
            else:
                data = response.data

            return data, 200

        except Exception as e:
            app.logger.error(e)
            return "Bad login", 401

    def add_item_to_table(self, access_token=None, app=None, data_dict=None,
                          table_name="entities_tracked",
                          ):
        try:
            self.sb_client.postgrest.auth(token=access_token)
            response = (
                self.sb_client.table(table_name)
                .insert(data_dict)
                .execute()
            )
            data = response.data

            return data, 200

        except Exception as e:
            app.logger.error(e)
            return "Bad login", 401


    def check_user_session(self, access_token=None, app=None,):
        """ check if user session is active
         >> reload data
         """

        try:
            res = self.sb_client.auth.get_session()
            data = res.data

            return data, 200

        except Exception as e:
            app.logger.error(e)
            return "Bad login", 401


    def log_out(self, access_token=None, app=None,):

        try:
            res = self.sb_client.auth.sign_out()
            data = res.data

            return data, 200

        except Exception as e:
            app.logger.error(e)
            return "Bad login", 401