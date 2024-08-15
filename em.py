""" EMAIL """
import os
from typing import List

import boto3
import dateutil
from dotenv import load_dotenv

from datetime import datetime
import dateutil

from airium import Airium

import constants

class EmailInterface:
    """ To access functions, set dummy=True"""

    def __init__(self, from_address=None,
                 email_addresses=None,
                 scrape_date="",
                 dummy=False,
                 supa_wrapper=None):
        load_dotenv()
        # Set your AWS region
        aws_region = 'us-east-1'
        self.from_addr = os.getenv('FROM_ADDRESS')  # returns str
        self.scrape_date = scrape_date

        # Create an SES client
        self.ses_client = boto3.client('ses', region_name=aws_region)

        # supa
        # self.supa = SupaClientWrapper()  # local wrapper
        self.supa = supa_wrapper

        """ SUPABASE """
        if not dummy:
            self.email_addresses = email_addresses
            if email_addresses is None:
                self.email_addresses = self.supa.get_all_email_addresses()


        return

    def send_all_emails(self, all_data: List, email_subject='NYC Transactions - Test',
                        email_addresses=None,
                        style=None):
        """
        given list of all mortgage and deed data,
        format string and send email
        to all gathered addresses
        """

        if style is None:
            email_body = self.basic_format_email_body(all_data=all_data)
        else:
            email_body = self.format_email_body(all_data=all_data)

        for addr in self.email_addresses:
            try:
                self.send_email(email_body=email_body,
                                email_subject=email_subject,
                                recipient_email=addr,
                                sender_email=self.from_addr)
            except BaseException as e:
                print(e, "bad email")

    def basic_format_email_body(self, all_data: List, date=""):
        """
        """
        s = str(self.scrape_date) + " \n"
        s += "\n ADDR / BORO / AMT / Party 1 / Party 2 / Doc ID No. \n"
        ctr = 0
        for li in all_data:
            if ctr % 5 == 0:
                print('\n')
            sub = ""
            for x in li:
                x = str(x)
                if x[0] == "$":
                    x = " " + x
                sub += " / " + x
            sub += "\n"
            s += sub

        return s

    def format_email_body(self, all_data: List):
        a = Airium()
        with a.table(id='all_data'):
            with a.tr(klass='header_row'):
                a.th(_t='no.')
                a.th(_t='Address')
                a.th(_t='Boro')
                a.th(_t='Amount')
                a.th(_t='Party 1')
                a.th(_t='Party 2')
                a.th(_t='Doc ID No.')

            for li in all_data:
                li = str(li)
                with a.tr():
                    a.td(_t=li)

            # with a.tr():
            #     a.td(_t='1.')
            #     a.td(id='jbl', _t='Jill')
            #     a.td(_t='Smith')  # can use _t or text
        return str(a)


    def send_email(self,
                   email_body: str,
                   email_subject='NYC Transactions - Test',
                   recipient_email='nyctransactions@gmail.com',
                   sender_email=None,):
        # Specify the email subject and body
        # email_subject = 'Test Email'
        # email_body = 'This is a test email sent from AWS SES using Python.'

        # Send the email
        response = self.ses_client.send_email(
            Source=self.from_addr,
            Destination={
                'ToAddresses': [recipient_email],
            },
            Message={
                'Subject': {'Data': email_subject},
                'Body': {'Text': {'Data': email_body}},
            }
        )

        print("Email sent! Message ID:", response['MessageId'])

    def test_send_email(self, email_body="TEST BODY",
                        email_subject='NYC Transactions - Test',
                        recipient_email='drborcich@gmail.com',
                        sender_email=None,):

        email_body = self.basic_format_email_body(all_data=[""], date="01/02/2024")

        self.send_email(email_body=email_body,
                        email_subject=email_subject,
                        recipient_email=recipient_email)



    def send_email_html(self,
                        email_body_raw_data: List,
                        email_subject='NYC Transactions - Test',
                        recipient_email='nyctransactions@gmail.com',
                        sender_email='nyctransactions@gmail.com',
                        cols=None,
                        no_results=False
                        ):
        """ email body data:
        if no results, NO_RES email insert
        """
        if no_results is True:
            with open('no_results.txt', 'r') as f:
                email_body_html = f.read()
        else:
            email_body_html = self.get_email_html(raw_data=email_body_raw_data,
                                                  cols=cols)

        # Send the email
        response = self.ses_client.send_email(
            Source=self.from_addr,
            Destination={
                'ToAddresses': [recipient_email],
            },
            Message={
                'Body': {
                    'Html': {
                        'Data': email_body_html,
                    },
                },
                'Subject': {
                    'Data': str(email_subject),
                },
            }
        )

        print("Email sent! Message ID:", response['MessageId'])

    def get_email_html(self, raw_data=None, cols=None,
                       sample_file='html_.txt',
                       combine_address=True
                       ):
        """ sort the keys for consistency! """
        """ expecting list of dicts """
        a = Airium()
        if not cols:
            sorted_keys = sorted(list(raw_data[0].keys()))
            # DANGER
        else:
            # space seps !!! be careful
            sorted_keys = cols.split(",")

        """ dash if absent, combine house_no and street name """
        for row in raw_data:  # list of dicts
            assert type(row) is dict
            with a.tr():
                for k in sorted_keys:
                    if k == 'filing_date':
                        # row[k] = datetime.strptime(row[k], '%m-%d-%Y')
                        row[k] = row[k][:10]
                    if k == 'house_no':
                        s = row['street_name'] if row['street_name'] else ""
                        r = str(row['house_no']) + " " + s
                        a.td(_t=r) if (k in row or row[k] != "NULL") else a.td(_t=constants.DASH)
                    elif k != 'street_name':
                        row[k] = constants.DASH if row[k] == "NULL" else row[k]
                        a.td(_t=row[k]) if (k in row or row[k] != "NULL") else a.td(_t=constants.DASH)

                    # a.td(_t=row[k])
        table_str = str(a)
        full_email_html = self.fill_email_html(table=table_str,
                                               cols=cols)
        with open(sample_file, 'w') as f:
            f.write(full_email_html)
        return full_email_html

    def sample_html(self):
        with open('sample_email.txt', 'r') as f:
            html = f.read()
        html = html.replace('\n', '')
        print(html)
        return html

    def fill_email_html(self, table, cols=None,):
        """
        TO DO: allow custom cols
        returns a string
        """
        with open('cust_cols_email.txt', 'r') as f:
            html = f.read()
        # update 8.7.24
        html = html.replace(constants.HTML_HEADERS_INS_LOC, constants.HTML_AUG_24_EMAIL_COLS)
        html = html.replace('\n', '')
        print(html)
        html = html.replace(constants.HTML_BODY_INS_LOC, table)
        return html

    def template_table_js(self, raw_data=None, cols=None,
                          ):
        """ sort the keys for consistency!
         raw_data = list[dict]
         """
        a = Airium(source_line_break_character="")
        if raw_data == []:  # 8/15/24
            return "<div> No data posted. </div>"
        if not cols:
            sorted_keys = sorted(list(raw_data[0].keys()))
            # DANGER
        else:
            # space seps !!! be careful
            sorted_keys = cols.split(",")
        # SANITIZE !
        san = ["user_id", "User_id", "Created_at"]  # 7/30
        for key in sorted_keys:
            if key in san:
                sorted_keys.remove(key)

        for row in raw_data:  # a dict
            assert type(row) is dict
            with a.tr():
                for k in sorted_keys:
                    if k in ['filing_date', 'created_at', 'current_status_date', 'permit_issue_date']:
                        if row[k] and row[k] != constants.NULL:
                            dt = dateutil.parser.parse(row[k])
                            row[k] = datetime.strftime(dt, '%m-%d-%Y %H:%M')
                        # row[k] = row[k][:10]
                    a.td(_t=row[k])

        # header = constants.ALL_DATA_FETCH_TABLE_HEADER
        header = self.create_table_headers(sorted_keys)
        table_str = "<table>" + header + str(a) + "</table>"

        return table_str

    def create_table_headers(self, headers_list):
        result = "<thead>"
        for h in headers_list:
            li = h.replace("_", " ").split(" ")
            li = [x.capitalize() + " " for x in li]
            h = "".join(li)
            h = "ID" if h == "Id " else h
            h = "Owner's Business Name" if h == "Owner S Business Name " else h
            h = h[:len(h)]  # remove trailing space
            result += "<th>" + h + " </th>"
        result = result + "</thead>"
        return result
