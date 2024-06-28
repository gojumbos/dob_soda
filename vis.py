

import json

data = json.load(open('6_12.json'))

for x in data[0].items():
    print(x)

print(len(data))
#
# j = data[0]
# for k in j.keys():
#     print(k)