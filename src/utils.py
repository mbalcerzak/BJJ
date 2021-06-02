import pandas as pd


def bjj_data_no_brackets():
    df = pd.read_csv('https://raw.githubusercontent.com/mbalcerzak/BJJ/master/Data/data_bjj.csv', sep=';')

    for col in list(df):
        df[col] = df[col].apply(lambda x: x.replace("[", "").replace("]", "").replace("\'", "").replace("\n", ""))

    df.to_csv('data_bjj_no_brackets.csv', sep=";")

    return df
