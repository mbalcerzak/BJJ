import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import altair as alt

st.title('BJJ  Survey 2017')

DATE_COLUMN = 'date/time'
#DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

path = r"C:\Users\malgo_000\Desktop\BJJ"
DATA_URL = path + r'\data_submissions.csv'

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data... done!')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

    
belts = ['I do not hold a rank', 'White Belt','Blue Belt', 'Purple Belt',
       'Brown Belt', 'Black Belt', 'no answer']    

   
st.write("Choose a belt you want to see the result for")
show_all = st.checkbox("Show all the answers")  
belt_chosen = st.radio("Current rank", belts)
   
if show_all:
    data = data
else:
    data = data[data['belt'] == belt_chosen]
    
question = 'technique'
question_list = data[question][data[question] != '']    
counts = OrderedDict(Counter(question_list[2:]).most_common())
    
data_bars = pd.DataFrame({'techniques':list(counts.keys()), 'count':list(counts.values())})

data_bars = data_bars.sort_values(by='count')

bars = alt.Chart(data_bars, height = 500, width = 400).mark_bar(color='steelblue', opacity=0.9).encode(
                x = alt.X('techniques', sort = None),
                y = 'count')
st.altair_chart(bars)

#    
#def bar_plot(question):
#    question_list = data[question][data[question] != '']
#    #data[question][data[question] == ''] = 'No answer'
#    
#    counts = OrderedDict(Counter(question_list[2:]).most_common())
#    
#    plt.bar(range(len(counts)), list(counts.values()), align='center')
#    plt.xticks(range(len(counts)), list(counts.keys()))
#    plt.xticks(rotation=45)
#    
#    st.pyplot()
#    
#bar_plot('technique')

#genders = ['Male', 'Female', 'no answer']

#st.write("Choose a gender you want to see the result for")
#gender_chosen = st.radio("Current rank", genders) 
#
#if show_all:
#    data2 = data
#else:
#    data2 = data[data['gender'] == gender_chosen]
#    
#def bar_plot(question):
#    question_list = data2[question][data2[question] != '']
#    #data[question][data[question] == ''] = 'No answer'
#    
#    counts = OrderedDict(Counter(question_list[2:]).most_common())
#    
#    plt.bar(range(len(counts)), list(counts.values()), align='center')
#    plt.xticks(range(len(counts)), list(counts.keys()))
#    plt.xticks(rotation=45)
#    
#    st.pyplot()
#    
#bar_plot('technique')

#st.subheader('Number of pickups by hour')
#hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
#st.bar_chart(hist_values)
#
## Some number in the range 0-23
#hour_to_filter = st.slider('hour', 0, 23, 17)
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#
#st.subheader('Map of all pickups at %s:00' % hour_to_filter)
#st.map(filtered_data)