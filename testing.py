


import em

import supa

sw = supa.SupaClientWrapper(service=True)

dt = [{"house_no": 1991, "bin": "00001"}, {"house_no": 343, "bin": "3333"}]

r, r2 = sw.overwrite_yday_table(data_dict=dt)

print(r, r2)

r = sw.write_yday_to_persist(data_dict=dt)

print(r,)