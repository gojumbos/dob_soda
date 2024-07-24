import json
import os
from datetime import datetime, timedelta
from typing import List

from flask import jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

import requests

import em

import supa

import constants


def dob_get_new_data(date_pre, date_post, token, logger=None,
                     cols=None, write_to_disk=False,
                     ):

    """ Job application filings """
    """ returns a list of dicts """

    # url = 'https://data.cityofnewyork.us/resource/w9ak-ipjd.json' + f'$$app_token={token}'
    # soql = '?$select=street_name,house_no&$where=permit_issue_date>\'2024-06-01T00:00:00.000\''

    f_date_pre = date_pre.strftime("%Y-%m-%d")    # earlier
    f_date_post = date_post.strftime("%Y-%m-%d")  # later

    default_cols_str = constants.DEFAULT_SODA_COLS if cols is None else cols

    soql1 = f'?$select={default_cols_str}&'
    # """ current_status_date - filing date """
    # soql2 = '$where=permit_issue_date between \'2024-06-10T00:00:00.000\' and \'2024-06-12T00:00:00.000\''  # date
    soql2 = f'$where=current_status_date between \'{f_date_pre}T00:00:00.000\' and \'{f_date_post}T00:00:00.000\''  # date

    file_type = 'json'  # json
    url = f'https://data.cityofnewyork.us/resource/w9ak-ipjd.{file_type}' + soql1 + soql2
    headers = {'X-App-Token': token}

    # task = asyncio.create_task(make_request(url=url, headers=headers))
    # r = asyncio.run(requests.get(url, headers=headers))
    r = requests.get(url, headers=headers)
    """ insert nulls """
    res = r.json()  # list of dicts
    col_list = default_cols_str.split(',')
    for d in col_list:
        for item in res:
            if d not in item:
                item[d] = "NULL"

    print(r.status_code)
    print(r.headers['content-type'], r.encoding)
    if write_to_disk:
        with open(f'{str(f_date_post)}.json', 'w') as f:
            json.dump(r.json(), f)

    return res


def cron_run():
    """ run daily cron job from api call"""
    """ service role required """

    service_supa_w = supa.SupaClientWrapper(service=True)
    col = 'created_at'

    tables = {'building': 'buildings_tracked',
              'entity': 'entities_tracked',
              'filing': 'filings_tracked'
              }

    """ GET DATA - SODA """
    today = datetime.today()
    prev_day = datetime.now() - timedelta(days=1)
    if today.weekday() == 0:  # if monday >> get friday
        prev_day = today - timedelta(days=3)
    token = constants.SODA_TOKEN
    # list of dicts
    soda_data_dict = dob_get_new_data(date_pre=prev_day,
                                 date_post=today,
                                 token=token,
                                 )

    # cols = "bin,owner_s_business_name,house_no,street_name,borough,filing_date,filing_status"

    """ WRITE TO SUPA """
    #
    r1 = service_supa_w.write_yday_to_persist(data_dict=soda_data_dict, )
    r2, r3 = service_supa_w.overwrite_yday_table(data_dict=soda_data_dict,)

    """ READ FROM SUPA - CHECK AGAINST ALL ITEM TYPES """
    """ for all users, check against all items """
    # supa: dict(list(dict))
    b_dict, e_dict = service_supa_w.check_all_tables(jay_data_list=soda_data_dict)

    # read table >> entities tracked
    # " >> buildings tracked
    # " >> filings tracked
    # check against r1, r2, r3

    """ EMAIL """
    emi = em.EmailInterface(dummy=True, supa_wrapper=service_supa_w, )

    # 6/26 - added bin no.
    # cols = "bin,owner_s_business_name,house_no,street_name,borough,filing_date,filing_status"

    email_li_dict = service_supa_w.get_all_users()

    send = True
    if send:
        for di in email_li_dict:
            uid, email_add = di['user_id'], di['email_address']
            b = b_dict[uid] if uid in b_dict else [{}]
            # e = "".join(e_dict[uid]) if uid in e_dict else "NULL"
            e = e_dict[uid] if uid in e_dict else [{"NULL": "NULL"}]
            b.extend(e)

            # s >> LIST OF DICTS, each dict is a match record
            emi.send_email_html(
                email_body_raw_data=b,
                cols=constants.ENTITY_COLS,
                recipient_email=email_add
            )

    return 200








