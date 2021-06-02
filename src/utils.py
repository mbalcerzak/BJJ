from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import json


def bjj_data_no_brackets():
    df = pd.read_csv('https://raw.githubusercontent.com/mbalcerzak/BJJ/master/Data/data_bjj.csv', sep=';')

    for col in list(df):
        df[col] = df[col].apply(lambda x: x.replace("[", "").replace("]", "").replace("\'", "").replace("\n", ""))

    df.to_csv('data_bjj_no_brackets.csv', sep=";")

    return df


def wordcloud_from_column(column):
    df = pd.read_csv('Data/data_bjj_no_brackets.csv', sep=";", index_col=[0])

    selected_column = df[column].loc[df[column] != "no answer"]
    value_list = selected_column.to_list()

    comment_words = ''
    stopwords = set(STOPWORDS)

    for val in value_list:
        val = str(val)
        tokens = val.split(',')
        print(tokens)

        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        comment_words += " ".join(tokens) + " "

    wordcloud = WordCloud(width=1200, height=1000,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=6).generate(comment_words)

    plt.figure(figsize=(12, 10), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.savefig(f'images/wordcloud_{column}.png')


if __name__ == '__main__':
    pass
