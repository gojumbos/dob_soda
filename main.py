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


def dob_get_new_data(date_pre, date_post, token, logger,
                     cols=None):

    """ Job application filings """

    # url = 'https://data.cityofnewyork.us/resource/w9ak-ipjd.json' + f'$$app_token={token}'
    # soql = '?$select=street_name,house_no&$where=permit_issue_date>\'2024-06-01T00:00:00.000\''

    f_date_pre = date_pre.strftime("%Y-%m-%d")    # earlier
    f_date_post = date_post.strftime("%Y-%m-%d")  # later

    default_cols = constants.DEFAULT_SODA_COLS if cols is None else cols

    soql1 = f'?$select={default_cols}&'
    # soql2 = '$where=permit_issue_date between \'2024-06-10T00:00:00.000\' and \'2024-06-12T00:00:00.000\''  # date
    soql2 = f'$where=filing_date between \'{f_date_pre}T00:00:00.000\' and \'{f_date_post}T00:00:00.000\''  # date

    file_type = 'json'  # json
    url = f'https://data.cityofnewyork.us/resource/w9ak-ipjd.{file_type}' + soql1 + soql2
    headers = {'X-App-Token': token}

    # task = asyncio.create_task(make_request(url=url, headers=headers))
    # r = asyncio.run(requests.get(url, headers=headers))
    r = requests.get(url, headers=headers)

    print(r.status_code)
    print(r.headers['content-type'], r.encoding)
    # print(r.text)
    # print(r.json())
    with open(f'{str(f_date_post)}.json', 'w') as f:
        json.dump(r.json(), f)

    # with open('all_data_job_app.csv', newline='') as csvfile:
    #     wrt = csv.writer(csvfile, delimiter=' ', quotechar='|')
    #     for row in wrt:
    #         print(', '.join(row))

    return r.json()


def supa_get_yesterday_data(logger, supa_client: SupaClientWrapper):
    """ get data from supa db """
    return


def supa_write_yesterday_data(data: list, supa_client: SupaClientWrapper, logger):
    return


def main(prev_step_back=1):
    supa_wrapper = SupaClientWrapper()
    logger = logging.getLogger('logger')

    """ dob updates on weekends ! """
    today = datetime.today()
    # prev_day = None
    # if today.weekday() == 0:
    #     prev_day = today - timedelta(days=3)
    # elif today.weekday() == 6:
    #     # logger.error('Today is Sunday')
    #     # return
    #     pass
    # elif today.weekday() == 5:
    #     # logger.error('Today is Saturday')
    #     pass
    # else:
    #     prev_day = datetime.now() - timedelta(days=1)
    prev_step_back = 1 if prev_step_back is None else prev_step_back
    prev_day = datetime.now() - timedelta(days=int(prev_step_back))

    token = constants.SODA_TOKEN
    token_sec = "RwclQaOeEK3K09Pf1OnuZTGQ9e8g8the-oBT"

    cols = "bin,owner_s_business_name,house_no,street_name,borough,filing_date,filing_status"

    # r.text ->
    data = dob_get_new_data(date_post=today, date_pre=prev_day, token=token, logger=logger,
                            cols=cols)

    email = em.EmailInterface(dummy=True, supa_wrapper=supa_wrapper,)

    # 6/26 - added bin no.


    send = True
    if send:
        email.send_email_html(
                              email_body_raw_data=data,
                              cols=cols
                              )
        email.send_email_html(
            email_body_raw_data=data,
            cols=cols,
            recipient_email='drborcich@gmail.com'
        )

    # dob_get_new_data(date_post=today,date_pre=prev_day,token=token,logger=logger)

    #
    # with open('all_data_job_app.csv', newline='') as csvfile:
    #     wrt = csv.writer(csvfile, delimiter=' ', quotechar='|')
    #     for row in wrt:
    #         print(', '.join(row))
    # with open('2024-06-13.json', 'r') as f:
    #     json_data = json.load(f)
    # table = 'job_apps_yesterday'
    #
    # for row in json_data:
    #     for k in SUPA_JAY_DB_COLS:
    #         if k not in row:
    #             print(k)
    #             row[k] = "NULL"
    #
    #
    # data, count = (supa_wrapper.sb_client.table(table)
    #                .insert(json_data)
    #                .execute())
    # print(data)
    # print("CT", count)


if __name__ == '__main__':
    # asyncio.run(main())
    parser = ArgumentParser()
    parser.add_argument("--prev_day", action="store", )

    args = parser.parse_args()
    main(prev_step_back=args.prev_day,)




