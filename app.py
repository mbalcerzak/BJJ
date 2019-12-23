import streamlit as st
import pandas as pd
#import os
from collections import Counter, OrderedDict
import altair as alt

st.title('BJJ  Survey 2017')

#DATA_URL = ('https://raw.githubusercontent.com/mbalcerzak/BJJ/master/Data/info/subs_info.csv')
DATA_URL = r'C:\Users\malgo_000\Documents\GitHub\BJJ\Data'

#@st.cache
def load_data(file_name):
    data = pd.read_csv(DATA_URL + r'\{}.csv'.format(file_name), sep = ';')
    return data

data_load_state = st.text('Loading data...')

data_view = load_data("data_bjj") # the one that has a pre-view

data_subs = load_data(r"info\subs_info") # submissions
data = load_data(r"info\training_info") # most of the information
data_back_ma = load_data(r"info\background_info")


data_load_state.text('Loading data... done!')

st.sidebar.text("github.com/mbalcerzak")

if st.checkbox('Show the data used for analysis'):
    st.subheader('Answers')
    st.write(data_view)
   
all_answers = "Overall"   

st.sidebar.header("Overall results or for a selected group?")

all_or_not = st.sidebar.radio("",[all_answers,'Selected'])

col_dictionary = {'white belt':'gray',
                 'blue belt':'steelblue', 
                 'purple belt':'rebeccapurple',
                 'brown belt':'sienna', 
                 'black belt':'black',
                 'no rank':'olivedrab',
                 'all belts':'olivedrab'}


belts = ['all belts', 'white belt','blue belt', 'purple belt', 'brown belt', 
         'black belt', 'no rank']  

genders = ['Every gender', 'Male','Female']

belt_chosen = belts[0]
gender_chosen = genders[0]

if all_or_not == 'Selected':
    st.sidebar.header("Choose a group")
    
    belt_chosen = st.sidebar.selectbox("Rank of survey participants:", belts)
    gender_chosen = st.sidebar.selectbox("Gender:", genders)  
    
    title_group = ": {}, {}".format(gender_chosen, belt_chosen)
    
else:
    title_group = ""
    
colour = col_dictionary[belt_chosen]

    
def filter_data(data, belt_chosen, gender_chosen):
    
    if belt_chosen != belts[0]:
        data = data[data['current_belt'] == belt_chosen]
    
    data = data[data['current_belt'] != 'no answer']
        
    if gender_chosen != genders[0]:    
        data = data[data['gender'] == gender_chosen]
    
    data = data[data['gender'] != 'no answer']
    
    return data

data_subs = filter_data(data_subs, belt_chosen, gender_chosen)

########### to change into a function later ##################################

data_bars = len(list(set(data_subs['technique'].to_list())))

if data_bars > 0:
    
    st.subheader("Favourite submissions{}".format(title_group))

    bars = alt.Chart(data_subs, height = data_bars * 16).mark_bar(
                        color = colour, opacity=0.9).encode(
                        x = alt.X('count(current_belt)', 
                              title = 'Number of times mentioned'),
                        y = alt.Y('technique', 
                                  sort = alt.EncodingSortField(
                                              field='current_belt', 
                                              op="count", 
                                              order='ascending'),
                              title = 'Favourite submissions'),
                        tooltip = 'count(current_belt)')
    
    #st.altair_chart(bars)

else:
    st.text('No data to show for {} & {}'. \
            format(belt_chosen.upper(),gender_chosen.upper()))

##############################################################################

# NORMALIZED STACKED BAR CHART 

#'Q67.1':'preferred_style'
data1 = filter_data(data, belt_chosen, gender_chosen)    
 
st.subheader("Preferred style of fighting{}".format(title_group))

order = belts[1:6]

def nomalised_barchart(data_, column, count_):
    
    data_ = data_[data_[column] != 'no answer']

    norm_bar = alt.Chart(data_).mark_bar().encode(
        y=alt.Y('current_belt', title = 'Current rank', sort = order),
        x=alt.X(count_, stack="normalize",
                title = 'Number of times mentioned',
                axis=alt.Axis(format='%')),
        color=column,
        tooltip = count_,
        order=alt.Order(
          column,
          sort = 'ascending'
        )
    )

#    text = alt.Chart(data_).mark_text(dx=-10, dy=3, color='black').encode(
#        x=alt.X(count_, stack="normalize", 
#                order=alt.Order( column,
#                                 sort = 'ascending')),
#        y=alt.Y('current_belt', sort = order),
#        detail=column,
#        text=alt.Text(count_)
#    )

    st.altair_chart(norm_bar) #+ text)
   
nomalised_barchart(data1, 'preferred_style','count(preferred_style)')    
    


#'Q3':'training_years',
st.subheader("Number of training years{}".format(title_group))
nomalised_barchart(data1, 'training_years','count(training_years)')  


#'Q6':'white_blue',
#'Q7':'blue_purple',
#'Q8':'purple_brown',
#'Q9':'brown_black',


#alt.Chart(source).mark_bar().encode(
#    x='sum(yield):Q',
#    y='year:O',
#    color='year:N',
#    row='site:N'
#)


#'Q10':'training_per_week', 
st.subheader("How often do you train per week{}".format(title_group))
nomalised_barchart(data1, 'training_per_week','count(training_per_week)') 


#'Q14':'training_time',
st.subheader("What time of day do you prefer to train{}".format(title_group))
nomalised_barchart(data1, 'training_time','count(training_time)')  


#'Q22':'how_old_when_started',
st.subheader("How old were you when you started{}".format(title_group))
nomalised_barchart(data1, 'how_old_when_started','count(how_old_when_started)')  

#'Q16':'travel',    # YES/NO
  
#'Q11':'both_gi_nogi', # YES/NO
#'Q12':'gi_or_no_gi', # YES/NO


#'Q17':'background_ma',
data_back_ma = filter_data(data_back_ma, belt_chosen, gender_chosen)  
st.subheader("Previously trained other martial art{}".format(title_group))
nomalised_barchart(data_back_ma, 'background_ma','count(background_ma)') 


#'Q30':'currently_cross_train', # YES/NO

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