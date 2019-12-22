import streamlit as st
import pandas as pd
#import os
from collections import Counter, OrderedDict
import altair as alt

st.title('BJJ  Survey 2017')

DATA_URL = ('https://raw.githubusercontent.com/mbalcerzak/BJJ/master/Data/data_bjj.csv')

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
   
all_answers = "Overall"   

st.sidebar.header("Would you like to see overall results or for a selected group?")

all_or_not = st.sidebar.radio("",[all_answers,'Selected'])
 
    
belts = ['white belt','blue belt', 'purple belt', 'brown belt', 
         'black belt', 'no rank']    


col_dictionary = {all_answers:'olivedrab',
                 'no rank':'olivedrab', 
                 'white belt':'gray',
                 'blue belt':'steelblue', 
                 'purple belt':'rebeccapurple',
                 'brown belt':'sienna', 
                 'black belt':'black'}


if all_or_not == 'Selected':
    st.sidebar.header("Choose a group")
    
    belt_chosen = st.sidebar.selectbox("Rank of survey participants:", belts)
 
    data = data[data['current_belt'] == belt_chosen]

    colour = col_dictionary[belt_chosen]
    
    everyone = 'Every gender'
    
    genders = [everyone, 'Male','Female']
    gender_chosen = st.sidebar.selectbox("Gender:", genders)
        
    if gender_chosen == everyone:
        pass
    else:
        data = data[data['gender'] == gender_chosen]

else:
    colour = col_dictionary[all_answers]

question = 'technique'
question_no_empty = data[question][data[question].str.len() > 0].to_list()
question_list = [x for y in question_no_empty for x in y if x != 'no answer'] 

st.subheader("Favourite techniques")

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


# NORMALIZED STACKED BAR CHART 

#'Q67.1':'preferred_style'
st.subheader("Preferred style of fighting")

data1 = data[data['current_belt'] != 'no answer']
data1 = data1[data1['preferred_style'] != 'no answer']

norm_bar = alt.Chart(data1).mark_bar().encode(
    y=alt.Y('current_belt'),
    x=alt.X('count(preferred_style)', stack="normalize"),
    color='preferred_style',
    tooltip = 'count(preferred_style)',
)

text = alt.Chart(data1).mark_text(dx=-10, dy=3, color='black').encode(
    x=alt.X('count(preferred_style)', stack="normalize"),
    y=alt.Y('current_belt'),
    detail='preferred_style',
    text=alt.Text('count(preferred_style)')
)



st.altair_chart(norm_bar + text)





#'Q3':'training_years',
#'Q22':'how_old_when_started',
#'Q6':'white_blue',
#'Q7':'blue_purple',
#'Q8':'purple_brown',
#'Q9':'brown_black',
#'Q10':'training_per_week',      
#'Q11':'both_gi_nogi',
#'Q12':'gi_or_no_gi',

#'Q14':'training_time',
#'Q16':'travel',  
#'Q17':'background_ma',
#'Q30':'currently_cross_train',

#'Q31':'mobility_exercises',
#'Q32':'yoga',  
  
#'Q66.1':'leg_lock_friendly',
#'Q27':'gym_curriculum',    
#'Q13':'gym_self_defense',  
    
#'Q23':'instrutor_encourages_competition',
#'Q24':'competed',
#'Q25':'medals',
#'Q26':'competition_organisaiton',
  
#'Q33':'num_gis',
#'Q35':'num_rashguards',
#'Q38':'num_shorts',
#'Q42':'bjj_apparel',
#'Q47':'money_for_gear', # percent of income
#'Q48':'membership',
    
#'Q56':'education',
#'Q55':'gender',
#'Q57':'age',
#'Q57.1':'income',
#'Q59':'race',
#'Q67':'nationality',
    
#'Q49':'time_watching_bjj',    
#'Q60':'do_watch_sport_bjj',
#'Q61.1':'where_watch_sport_bjj',
#'Q62':'have_fav_athlete',

#'Q44':'Have you ever had a problem with a particular manufacturer or brand?',
#'Q18':'Why did you start training jiu jitsu?',
#'Q19':'What is your favorite part about training?',
#'Q20':'What is your least favorite part about training?',
#'Q61.1':'If you do watch sport jiu jitsu, what do you watch and where do you watch it?',
#'Q63':'Who are your favorite athletes (if any)?'