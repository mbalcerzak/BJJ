import streamlit as st
import pandas as pd
#import os
from collections import Counter, OrderedDict
import altair as alt

st.title('BJJ  Survey 2017')

#DATA_URL = ('https://raw.githubusercontent.com/mbalcerzak/BJJ/master/Data/data_bjj.csv')
DATA_URL = r"C:\Users\malgo_000\Documents\GitHub\BJJ\Data\data_bjj.csv"
#@st.cache
def load_data():
    data = pd.read_csv(DATA_URL, sep = ';')
    for column in list(data):
        if '[' in data[column][0]:

            data[column] = data[column].apply(lambda x: x[1:-1].split(','))
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('Loading data... done!')

st.sidebar.text("github.com/mbalcerzak")


if st.checkbox('Show the data used for analysis'):
    st.subheader('Answers')
    st.write(data)
   
all_answers = "All answers"    
    
belts = [all_answers, 'white belt','blue belt', 'purple belt', 'brown belt', 
         'black belt', 'no rank']    


col_dictionary = {all_answers:'olivedrab',
                 'no rank':'olivedrab', 
                 'white belt':'gray',
                 'blue belt':'steelblue', 
                 'purple belt':'rebeccapurple',
                 'brown belt':'sienna', 
                 'black belt':'black'}

st.sidebar.header("Choose what data do you want to see")
belt_chosen = st.sidebar.selectbox("Current rank of survey participants", belts)
 
if belt_chosen == all_answers:
    pass
else:
    data = data[data['current_belt'] == belt_chosen]

colour = col_dictionary[belt_chosen]

all_answersg = 'Every gender'

genders = [all_answersg, 'Male','Female','no answer']

gender_chosen = st.sidebar.selectbox("Choose a gender you want to see the result for",
                                 genders)
    
if gender_chosen == all_answersg:
    pass
else:
    data = data[data['gender'] == gender_chosen]

question = 'technique'
question_no_empty = data[question][data[question].str.len() > 0].to_list()
question_list = [x for y in question_no_empty for x in y if x != 'no answer'] 

st.subheader("Favourite techhniques")

if len(question_list) == 0:
    st.text('No data to show for {} & {}'. \
                format(belt_chosen.upper(),gender_chosen.upper()))
else:
    
    counts = OrderedDict(Counter(question_list).most_common())
        
    data_bars = pd.DataFrame({'techniques':list(counts.keys()),
                              'count':list(counts.values())})
    
    data_bars = data_bars.sort_values(by='count')
    
    bar_height = len(data_bars) * 15
    
    bars = alt.Chart(data_bars, height = bar_height, width = 500).mark_bar(
                    color = colour, opacity=0.9).encode(
                        alt.Y('techniques', sort = None, 
                              title = 'Favourite submissions'),
                        alt.X('count', title = 'number of times mentioned'),
                        tooltip = 'count')
    
    st.altair_chart(bars)

