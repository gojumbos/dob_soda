
import requests
import json
import csv
import logging

from datetime import datetime, timedelta

from supa import SupaClientWrapper
import asyncio

from constants import SUPA_JAY_DB_COLS

import em


def dob_get_update(date_pre, date_post, token,
                   ):
    """
    """

    f_date_pre = date_pre.strftime("%Y-%m-%d")    # earlier
    f_date_post = date_post.strftime("%Y-%m-%d")  # later

    soql1 = ('?$select=street_name,house_no,borough,filing_status,job_filing_number,filing_date,' +
             'applicant_first_name,applicant_last_name, owner_s_business_name,filing_representative_business_name&')
    # soql2 = '$where=permit_issue_date between \'2024-06-10T00:00:00.000\' and \'2024-06-12T00:00:00.000\''  # date
    # soql2 = f'$where=filing_date between \'{f_date_pre}T00:00:00.000\' and \'{f_date_post}T00:00:00.000\''  # date
    soql2 = f'$where=current_status_date between \'{f_date_pre}T00:00:00.000\' and \'{f_date_post}T00:00:00.000\''  # date

    file_type = 'json'  # json
    url = f'https://data.cityofnewyork.us/resource/w9ak-ipjd.{file_type}' + soql1 + soql2
    headers = {'X-App-Token': token}

    # task = asyncio.create_task(make_request(url=url, headers=headers))
    # r = asyncio.run(requests.get(url, headers=headers))
    r = requests.get(url, headers=headers)

    print(r.status_code)
    print(r.headers['content-type'], r.encoding)
    # print(r.json())
    with open(f'{str(f_date_post)}.json', 'w') as f:
        json.dump(r.json(), f)

    # with open('all_data_job_app.csv', newline='') as csvfile:
    #     wrt = csv.writer(csvfile, delimiter=' ', quotechar='|')
    #     for row in wrt:
    #         print(', '.join(row))

    return r.status_code,


