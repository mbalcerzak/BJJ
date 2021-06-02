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


def get_belt_colours():
    with open('Dictionaries/belts.json', 'r') as f:
        file = json.load(f)
    return file["belts"]


def get_counts(data: pd.DataFrame = None, json_name: str = None) -> None:
    final_json = {}
    data["current_age"] = data["age"].apply(get_age_brackets)

    for col in list(data):
        data[col] = data[col].apply(lambda x: [x.strip() for x in x.split(",")])
        col_list = data[col].sum()
        answers = [x for x in col_list if x != "no answer"]
        col_count = dict(Counter(sorted(answers)))

        final_json[col] = col_count

    with open(f'{json_name}.json', 'w') as outfile:
        json.dump(final_json, outfile)


def create_belts_jsons():
    df = pd.read_csv('../Data/data_bjj_no_brackets.csv', sep=";", index_col=[0])
    all_belts = df.copy()

    get_counts(all_belts, "bjj_overall")

    belt_colours = get_belt_colours()

    for belt in belt_colours.keys():

        belt_df = df.loc[df['current_belt'] == belt]
        belt_df = belt_df.drop(columns=['current_belt'])

        assert len(belt_df) > 0

        get_counts(belt_df, belt_colours[belt])


def create_belt_gender_summaries():
    df = pd.read_csv('../Data/data_bjj_no_brackets.csv', sep=";", index_col=[0])

    df_copy = df.copy()

    belt_colours = get_belt_colours()
    genders = ["Female", "Male"]

    for gender in genders:
        gender_df = df.loc[df['gender'] == gender]
        gender_df = gender_df.drop(columns=['gender'])

        get_counts(gender_df, gender)

        for belt in belt_colours.keys():
            belt_df = df_copy.loc[(df_copy['current_belt'] == belt)]
            belt_df = belt_df.drop(columns=['current_belt'])

            if len(belt_df) > 0:
                get_counts(belt_df, f"{gender}_{belt_colours[belt]}")


if __name__ == "__main__":
    create_belt_gender_summaries()
