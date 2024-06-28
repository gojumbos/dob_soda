
import requests
import json
import csv
import logging

from datetime import datetime, timedelta

from supa import SupaClientWrapper
import asyncio

from constants import SUPA_JAY_DB_COLS

import em

# async def make_request(url, headers):
#     r = await requests.get(url, headers=headers)


def dob_check_item_last_update(date_pre, date_post, token, logger,
                               subject, col,
                               ):
    """

    """
    # soql1 = ('?$select=street_name,house_no,borough,filing_status,job_filing_number,filing_date,' +
    #          'applicant_first_name,applicant_last_name, owner_s_business_name,filing_representative_business_name&')
    soql1 = f'?select={col}&where=f{col}=f{subject}'
    soql2 = ""

    file_type = 'json'  # json
    url = f'https://data.cityofnewyork.us/resource/w9ak-ipjd.{file_type}' + soql1 + soql2
    headers = {'X-App-Token': token}

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json(), 200
    else:
        return "Bad request", r.status_code


