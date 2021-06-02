import pandas as pd
from collections import Counter
import json


def get_age_brackets(age:str = None) -> str:
    if age == "no answer":
        return age

    age = int(age)
    if age <= 10:
        cat = '0-10'
    elif age <= 15:
        cat = '11-15'
    elif age <= 20:
        cat = '16-20'
    elif age <= 25:
        cat = '21-25'
    elif age <= 30:
        cat = '26-30'
    elif age <= 35:
        cat = '31-35'
    elif age <= 40:
        cat = '36-40'
    else:
        cat = '40+'

    return cat.strip()


def main():
    df = pd.read_csv('data_bjj.csv', sep=';')
    final_json = {}

    df["current_age"] = df["age"].apply(get_age_brackets)

    for col in list(df):
        df[col] = df[col].apply(lambda x: x.replace("[", "").replace("]", "").replace("\'", ""))
        df[col] = df[col].apply(lambda x: [x.strip() for x in x.split(",")])
        col_list = df[col].sum()
        col_count = dict(Counter(sorted(col_list)))
        final_json[col] = col_count

    with open('bjj_overall.json', 'w') as outfile:
        json.dump(final_json, outfile)


if __name__ == "__main__":
    main()
