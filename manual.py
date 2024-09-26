import json
import pandas as pd
from airium import Airium

def raw_json(raw_data: list):
    a = Airium()

    with a.table(id='tablee'):
        for row in raw_data:  # list of dicts
            assert type(row) is dict
            with a.tr():
                # a.td(_t=r) if (k in row or row[k] != "NULL") else a.td(_t=constants.DASH)
                for v in row.values():
                    a.td(_t=str(v))
    table_str = str(a)
    return table_str


def test():

    day = "25"

    fp = f'_json/2024-09-{day}.json'

    with open(fp, 'r') as file:
        sc_data = json.load(file)

    print(sc_data)

    ef = 'entities_hrg/entities_tracked_rows.csv'
    bf = 'build_hrg/building_tracked_rows.csv'

    df = pd.read_csv(ef, dtype=str)
    df = df.drop(columns=['id', 'user_id', 'created_at'])


    res = []
    for index, row in df.iterrows():
        for col in df.columns:
            itm = str(df.at[index, col]).replace('\n', "")
            # print(itm)
            if col != "applicant_first_name" and len(itm) > 1:
                for dct in sc_data:
                    for k in dct:
                        if itm in dct[k]:
                            res.append([str(row), str(dct)])

    print(res)

if __name__ == '__main__':
    test()