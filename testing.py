import os

from dotenv import load_dotenv

import em

import supa
import constants
from cron import cron_run



r = cron_run(testing=True, time_diff=1)
load_dotenv()

print(os.getenv('CRON_KEY'))
print(r)

# sw = supa.SupaClientWrapper(service=True)
#
#
# # sw.supa_login(email='drborcich@gmail.com', password='@tfGG67BMxz!Mjj')
#
# dt = [{ "bin": "999999", "street_name": "aa"},
#       { "bin": "45454", },
#        {"house_no": 56565, "bin": "3", "id":-2}]
#
# # r, r2 = sw.overwrite_yday_table(data_dict=dt)
#
# # print(r, r2)
#
# # data = sw.read_table(limit=5)
# #
# filtered_data = sw.check_all_tables(jay_data_list=dt)
# print(filtered_data)

# here
# bt = "buildings_tracked"
# jay = "job_apps_yesterday"
# cols = constants.BUILD_COLS
# r = (
#     sw.sb_client.table("buildings_tracked")
#     .select(f"user_id, {jay}!inner({cols})")
#     .eq(f"{jay}.bin", f"{bt}.bin")
#     .execute()
# )


# r = sw.write_yday_to_persist(data_dict=dt)
