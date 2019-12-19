import pandas as pd
import os
import altair as alt
from collections import Counter, OrderedDict
import altair as alt
#alt.renderers.enable('html')
#path = os.getcwd()
data = pd.read_csv(r'C:\Users\malgo_000\Documents\GitHub\BJJ\data_bjj.csv', sep = ';')

for column in list(data):
    if '[' in data[column][0]:
        print('is a list')
        data[column] = data[column].apply(lambda x: x[1:-1].split(','))

belts = ['I do not hold a rank', 'White Belt','Blue Belt', 'Purple Belt',
         'Brown Belt', 'Black Belt', 'no answer']    

genders = ['Male','Female','no answer']
   
     
question = 'technique'
question_no_empty = data[question][data[question] != ''].to_list()
question_list = [x for y in question_no_empty for x in y]   
counts = OrderedDict(Counter(question_list[2:]).most_common())
    
data_bars = pd.DataFrame({'techniques':list(counts.keys()),
                          'count':list(counts.values())})

data_bars = data_bars.sort_values(by='count')

bars = alt.Chart(data_bars, height = 500, width = 400).mark_bar(color='steelblue', opacity=0.9).encode(
                x = alt.X('techniques', sort = None),
                y = 'count')

#bars.serve()