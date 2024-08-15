

SUPA_JAY_DB_COLS = ['house_no',
                    'street_name',
                    'borough',
                    'filing_status',
                    'job_filing_number',
                    'filing_date',
                    'applicant_first_name',
                    'applicant_last_name',
                    'owner_s_business_name',
                    'filing_representative_business_name'
                    ]


ALL_DATA_FETCH_TABLE_HEADER = ("<thead> <tr> <th>Owner Business Name "
                               "</th> <th>House No. </th> <th>Street "
                               "</th> <th>Borough</th> <th>Filing Date "
                               "</th> <th>Filing Status</th> </tr> </thead>")


# SODA_TOKEN = "gbW4sPjH0aZDjC0mdLxZOvItb"
SODA_TOKEN = 'Qvtzkfzq9iG3DKkDUKJvux3ZD'

DEFAULT_SODA_COLS = 'street_name,house_no,borough,filing_status,job_filing_number,filing_date,applicant_first_name,applicant_last_name,owner_s_business_name,filing_representative_business_name,permit_issue_date,bin,current_status_date'
DEFAULT_EMAIL_COLS = "bin,owner_s_business_name,house_no,street_name,borough,filing_date,filing_status"


# columns present in each item table
# BUILD_COLS = "bin,street_name,house_no,user_id" do not include user id
BUILD_COLS = "bin,street_name,house_no"
ENTITY_COLS = "applicant_first_name,applicant_last_name,applicant_license,filing_representative_business_name,owner_s_business_name"

# COLS_LIST = {BUILD_COLS: ""}
BUILD_LIST_COLS: list = BUILD_COLS.split(",")
ENT_LIST_COLS: list = ENTITY_COLS.split(",")

ALL_ITEM_TYPES = ('building', 'entity', 'filing')
SUPA_ITEM_TABLES = ('buildings_tracked', 'entities_tracked', 'filings_tracked')
SUPA_JAY = 'job_apps_yesterday'

SIMPLE_EMAIL_COLS = "bin,name"
# SIMPLE_ENTITY_COLS = "bin,applicant_first_name,applicant_last_name,applicant_license,filing_representative_business_name,owner_s_business_name"
SIMPLE_ENTITY_COLS = "bin,house_no,street_name,borough,applicant_first_name,applicant_last_name,filing_representative_business_name,owner_s_business_name"

HTML_BODY_INS_LOC = "XXX_"
HTML_HEADERS_INS_LOC = "YYY_"

# update aug 7 24:
AUG_24_EMAIL_COLS = "house_no,street_name,borough,applicant_first_name,applicant_last_name,filing_representative_business_name,owner_s_business_name"
HTML_AUG_24_EMAIL_COLS = ("<th> Address </th> " +
                      "<th> Boro </th>" +
                      "<th> Applicant First Name </th> " +
                      "<th> Applicant Last Name </th>" +
                      "<th> Filing Representative Business Name </th>" +
                      "<th> Owner's Business Name </th>"
                      )

HTML_ENT_LIST_COLS = ("<th>Bin </th> <th> Address </th> " +
                      "<th> Boro </th>" +
                      "<th> Applicant First Name </th> " +
                      "<th> Applicant Last Name </th>" +
                      "<th> Filing Representative Business Name </th>" +
                      "<th> Owner's Business Name </th>"
                      )

DASH = "--"
NULL = "NULL"

HOME_URL_DEV = 'http://127.0.0.1:8000/api'
HOME_URL_PROD = 'https://clownfish-app-8om3z.ondigitalocean.app/dob-soda2/api'

