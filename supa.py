

import os
from typing import List

from supabase import create_client, Client
from dotenv import load_dotenv

import constants


class SupaClientWrapper:
    def __init__(self, service=False):
        load_dotenv()
        print('service: ', service)
        self.service = service
        self.url: str = os.environ.get("SUPABASE_URL")
        # self.key = os.environ.get("SUPABASE_KEY")
        # self.sb_client: Client = create_client(self.url, self.key)

        if service:
            self.key: str = os.environ.get("DANGER_SUPABASE_SERVICE")  # service role
            self.sb_client: Client = create_client(self.url, self.key)
        else:
            # self.url: str = os.environ.get("SUPABASE_URL")
            self.key = os.environ.get("SUPABASE_KEY")
            self.sb_client: Client = create_client(self.url, self.key)
        return

    def clean_table_results(self, dict_):
        """ given a dict, None -> str(NULL) """
        for k in dict_.keys():
            if dict_[k] is None:
                dict_[k] = "NULL"
        return dict_

    def upd_check_all_tables(self, soda_data_dict=None):
        build_res, ent_res = {}, {}
        flat_ ={}

        """ collate all soda data """
        for d in soda_data_dict:
            for k in d.keys():
                if d[k] is not None:
                    p = (str(k).lower(), str(d[k]).lower())
                    if p not in flat_:
                        flat_[p] = []

        build_data_supa = self.check_item_table_for_updates(table_name="buildings_tracked")


        return build_res, ent_res

    def check_all_tables(self, soda_data_dict=None):
        """ check for id match against all 3 item tables, RET 2 DICT of LISTS OF DICTS
        BIN NUMBER REQUIRED,
        CURRENT COLS: BIN, FNAME, LNAME
        Entity search: can only match on one column (or first + last name),
            but can be any column in Entity List Cols,
        TAKE ENTIRE ~soda~ ROW (not for build)
        *** 7/29 >> return soda data, not supa
        """
        if soda_data_dict == []:
            return {}, {}
        build_res, ent_res = {}, {}
        # build_keys = constants.BUILD_LIST_COLS
        # build_keys = [x for x in build_keys if x != "user_id"]
        # tracked buildings:
        build_data_supa = self.check_item_table_for_updates(table_name="buildings_tracked")
        for build_row in build_data_supa:
            for soda_row in soda_data_dict:  # non supa
                key = "bin"
                if build_row[key] == soda_row[key]:
                    # build_res.append([build_row["user_id"], build_row["bin"]])
                    # build_res[build_row["user_id"]] = build_row["bin"]
                    if build_row["user_id"] not in build_res:
                        build_res[build_row["user_id"]] = []

                    # build_res[build_row["user_id"]].append({"bin": build_row["bin"]})
                    """ clean """
                    self.clean_table_results(dict_=soda_row)
                    build_res[build_row["user_id"]].append(soda_row)

        """ ENT """
        ent_data_supa = self.check_item_table_for_updates(table_name="entities_tracked")
        for ent_row in ent_data_supa:
            for soda_row in soda_data_dict:  # dict
                """ first name, last name => combined"""
                for col in constants.ENT_LIST_COLS:
                    if col == constants.ENT_LIST_COLS[0]:
                        afn, aln = constants.ENT_LIST_COLS[0], constants.ENT_LIST_COLS[1]
                        if (afn in soda_row and aln in soda_row):
                            if (ent_row[afn] and soda_row[afn]) and (ent_row[aln] and soda_row[aln]):
                                if ent_row[afn].lower() == soda_row[afn].lower() and ent_row[aln].lower() == soda_row[aln].lower():
                                    # ent_res[ent_row["user_id"]] = "" + str(ent_row[afn]) + " " + str(ent_row[aln])
                                    # ent_res[ent_row["user_id"]].append("" + str(ent_row[afn]) + " " + str(ent_row[aln]))
                                    if ent_row["user_id"] not in ent_res:
                                        ent_res[ent_row["user_id"]] = []
                                    """ clean """
                                    self.clean_table_results(dict_=soda_row)
                                    ent_res[ent_row["user_id"]].append(soda_row)
                    elif col != constants.ENT_LIST_COLS[1]:
                        """ RETURN THE WHOLE ROW """
                        if col and (col in soda_row and col in ent_row):
                            if ent_row[col] and soda_row[col]:
                                if ent_row[col].lower() == soda_row[col].lower():
                                    # ent_res[ent_row["user_id"]] = ent_row[col]
                                    if ent_row["user_id"] not in ent_res:
                                        ent_res[ent_row["user_id"]] = []
                                    # ent_res[ent_row["user_id"]] = ent_row
                                    """ clean"""
                                    self.clean_table_results(dict_=soda_row)
                                    ent_res[ent_row["user_id"]].append(soda_row)

        # filings_data_supa = self.check_item_table_for_updates(table_name="filings_tracked")
        """ CLEAN """

        return build_res, ent_res  # 2 dicts of lists of dicts

    def check_item_table_for_updates(self, table_name):
        """ read from item (entity, building, filing)
        return rows to be emailed
        FIX ME: should be replaced with supa trigger
        """
        data = self.read_table(table_name=table_name,)

        return data

    def write_yday_to_persist(self, data_dict=None):
        """ write data update to persist table """
        """ SERVICE ROLE! """
        if data_dict == []:
            return 200
        data, code = self.service_add_item_to_table(data_list_dicts=data_dict,
                                                    table_name='job_apps_persist')
        # if code != 200:
        #     raise Exception(f"Bad request {code} is not")
        return code

    def overwrite_yday_table(self, table_name="job_apps_yesterday",
                             data_dict=None):
        """ delete and update table """
        """ delete all columns - (where id != -1) """
        """ INSERT: list of dicts """
        if data_dict == []:
            return 200, 200

        response1 = (self.sb_client.table("job_apps_yesterday")
                    .delete()
                    .neq('id',-1)
                    .execute())

        response2 = (self.sb_client.table("job_apps_yesterday")
                     .insert(data_dict).execute())

        return response1, response2

    def get_all_users(self):
        """ SERVICE ROLE - get all users """
        assert (self.service is True)
        data = self.read_table('all_users', col_names='user_id,email_address',
                               condition=("active","TRUE"))
        return data

    def read_table(self, table_name='job_apps_yesterday',
                   col_names='*',
                   limit=None,
                   condition=None
                   ):
        """ DEFAULT: read JAY table, all columns """
        """ condition: (str:<col>,str:<value>) """
        # 'job_filing_number'
        cols = col_names  # a str
        if condition:
            response = (self.sb_client.table(table_name=table_name)
                        .select(cols)
                        .eq(condition[0], condition[1])
                        .execute())
        else:
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

    def service_add_item_to_table(self, data_list_dicts=None,
                                  table_name='job_apps_persist'):
        """ service role only """
        try:
            response = (
                self.sb_client.table(table_name)
                .insert(data_list_dicts)
                .execute()
            )
            data = response.data

            return data, 200

        except Exception as e:
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