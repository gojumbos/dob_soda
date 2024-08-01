
"""
Search for matches
"""

from dotenv import load_dotenv
from flask import make_response, jsonify

import supa
from app import AppController


email = 'holden@hrgcap.com'
password = 'hrg'

sw = supa.SupaClientWrapper()
app_controller = AppController(supa_wrapper=sw)
app_ = app_controller.app_object
# logger = logging.getLogger('logger')
load_dotenv()


# supabase.auth.set_session(access_token=access_token, refresh_token=refresh_token)

token, code = sw.supa_login(email=email, password=password,
                                      app=app_)
""" INSECURE: bypass RLS """

print(code)
# list of dicts:
text, code = sw.get_items(access_token=token,
                                        app=app_,
                                        table='entities_tracked',
                                        limit=None)
# list of dicts:
soda_ = sw.read_table()

flat_ = {}  # (key, d[key]) -> []

""" collate all soda data """
for d in soda_:
    for k in d.keys():
        if d[k] is not None:
            p = (str(k).lower(), str(d[k]).lower())
            if p not in flat_:
                flat_[p] = []

""" if any item from tracked is in soda """
for d in text:
    for key in d.keys():
        if (str(key).lower(), str(d[key]).lower()) in flat_ and d[key] is not None:
            print(">> ", key, d[key])

for d in text:
    for k, v in d.items():
        if k != "id":
            if str(v).lower() in str(flat_):
                print("in: ", k, v, )

print("done")



