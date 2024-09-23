from argparse import ArgumentParser

import requests
import json
import csv
import logging

from datetime import datetime, timedelta

from supa import SupaClientWrapper
import asyncio

import constants

import em

from cron import dob_get_new_data



def supa_get_yesterday_data(logger, supa_client: SupaClientWrapper):
    """ get data from supa db """
    return


def supa_write_yesterday_data(data: list, supa_client: SupaClientWrapper, logger):
    return


def main(prev_step_back=1):

    supa_wrapper = SupaClientWrapper(service=True)
    logger = logging.getLogger('logger')

    # email_dict = supa_wrapper.get_all_users()

    """ dob updates on weekends ! """

    # today = datetime.today()
    # prev_step_back = 1 if prev_step_back is None else prev_step_back
    # prev_day = datetime.now() - timedelta(days=int(prev_step_back))
    today = datetime.today()
    # prev_day = datetime.now() - timedelta(days=1)
    # today = datetime.today() - timedelta(days=)
    prev_day = datetime.now() - timedelta(days=3) # 9/18/24
    if today.weekday() == 0:  # if monday >> get friday
        prev_day = today - timedelta(days=3)
    token = constants.SODA_TOKEN
    # list of dicts
    data = dob_get_new_data(date_pre=prev_day,
                                      date_post=today,
                                      token=token,
                                      )

    token = constants.SODA_TOKEN
    token_sec = "RwclQaOeEK3K09Pf1OnuZTGQ9e8g8the-oBT"

    # cols = "bin,owner_s_business_name,house_no,street_name,borough,filing_date,filing_status"
    cols = constants.DEFAULT_SODA_COLS

    # r.text ->
    # data = dob_get_new_data(date_post=today, date_pre=prev_day, token=token, logger=logger,
    #                         cols=cols, write_to_disk=True)

    emi = em.EmailInterface(dummy=True, supa_wrapper=supa_wrapper,)

    # 6/26 - added bin no.

    # r1 = supa_wrapper.write_yday_to_persist(data_dict=data, )
    # r2, r3 = supa_wrapper.overwrite_yday_table(data_dict=data, )

    """ insert """
    data.append({'bin': '01010', })
    data.append({'bin': '8888', 'applicant_first_name': 'RUSSEL',
                 'applicant_last_name': 'PETERS'})
    data.append({'bin': '59161', 'applicant_first_name': 'Mike'})
    data.append({'bin': '3','filing_representative_business_name': 'Red'})
    data.append({'bin': '3','filing_representative_business_name': 'RED HOOK SIGN AND ELECTRI'})

    # partition data - by user
    # each user_id gets only the item-updates they subscribe to
    b_dict, e_dict = supa_wrapper.check_all_tables(soda_data_dict=data)
    # print(b_dict, e_dict)
    for b in b_dict:
        print(b, b_dict[b])
    for e in e_dict:
        print(e, e_dict[e])

    # email_li_dict = [
    #     {'user_id': '2e776a12-d0e9-4897-b2ba-1fa298d917ec',
    #      'email_address': 'drborcich@gmail.com'}
    #               ]
    # email_li_dict = supa_wrapper.get_all_users()

    email_li_dict = supa_wrapper.get_all_users()

    send = True
    if send:
        for di in email_li_dict:
            uid, email_add = di['user_id'], di['email_address']
            b = b_dict[uid] if uid in b_dict else [{}]
            # e = "".join(e_dict[uid]) if uid in e_dict else "NULL"
            e = e_dict[uid] if uid in e_dict else [{"NULL": "NULL"}]

            if b == [{}] and e == [{"NULL": "NULL"}]:
                """ Empty result email"""
                no_results = True
            else:
                no_results = False
            b.extend(e)
            # s >> LIST OF DICTS, each dict is a match record
            emi.send_email_html(
                email_body_raw_data=b,
                cols=constants.ENTITY_COLS,
                recipient_email=email_add,
                no_results=no_results
            )

    return 200




if __name__ == '__main__':
    # asyncio.run(main())
    parser = ArgumentParser()
    parser.add_argument("--prev_day", action="store", )

    args = parser.parse_args()
    main(prev_step_back=args.prev_day,)




