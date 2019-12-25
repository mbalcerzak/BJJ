import streamlit as st
import pandas as pd
#import os
from collections import Counter, OrderedDict
import altair as alt
import matplotlib.pyplot as plt

from Functions.for_streamlit.bygroups_app import bygroups_show

st.title('BJJ  Survey 2017')

#DATA_URL = ('https://raw.githubusercontent.com/mbalcerzak/BJJ/master/Data/info/subs_info.csv')
DATA_URL = r'C:\Users\malgo_000\Documents\GitHub\BJJ\Data'

#@st.cache

# ---------------------- LOADING DATA FROM GITHUB -------------------------- #
def load_data(file_name):
    data = pd.read_csv(DATA_URL + r'\{}.csv'.format(file_name), sep = ';')

    return data

data_load_state = st.text('Loading data...')

data_view = load_data("data_bjj") # the one that has a pre-view

data = load_data(r"info\training_info")
data_back_ma = load_data(r"info\background_info")
data_current_ma = load_data(r"info\current_ma_info")

data_subs = load_data(r"info\subs_info")
data_reasons = load_data(r"info\reasons_info")
data_least_f = load_data(r"info\least_f_info")
data_podcast = load_data(r"info\podcast_info")
data_web = load_data(r"info\web_info")
data_gi = load_data(r"info\gi_info")
data_rash = load_data(r"info\rash_info")
data_shorts = load_data(r"info\shorts_info")
data_apparel = load_data(r"info\apparel_info")
data_comp = load_data(r"info\comp_info")
data_injury = load_data(r"info\injury_info")
data_athlete = load_data(r"info\athlete_info")
data_watch = load_data(r"info\watch_info")

data_load_state.text('Loading data... done!')

# ----------------- FINISHED LOADING DATA FROM GITHUB ---------------------- #

st.sidebar.text("github.com/mbalcerzak")

if st.checkbox('Show the data used for analysis'):
    st.subheader('Answers')
    st.write(data_view)
   
st.sidebar.header("Overall results or for a selected group?")

all_or_not = st.sidebar.radio("",["Overall",
                                  'Show by groups',
                                  'Compare two groups'])

col_dictionary = {'white belt':'gray',
                  'blue belt':'steelblue', 
                  'purple belt':'rebeccapurple',
                  'brown belt':'sienna', 
                  'black belt':'black',
                  'no rank':'olivedrab',
                  'all belts':'olivedrab'}


belts = ['all belts', 
         'white belt','blue belt', 'purple belt', 'brown belt', 'black belt', 
         'no rank']  

genders = ['Every gender', 'Male','Female']

#belt_chosen = belts[0]
#gender_chosen = genders[0]

if all_or_not == 'Show by groups':
    
    st.sidebar.header("Split the answers by ...")
    by_group = st.sidebar.radio("",['Current rank','Gender'])

    by_gr_dict = {'Current rank':['current_belt', belts[1:6]],
                  'Gender':['gender', None]}    

    # include the function from by-groups module
    bygroups_show(data, data_back_ma, data_current_ma, by_gr_dict, by_group)

elif all_or_not == 'Compare two groups':
    
    st.sidebar.header("Compare:")
    belt_chosen_a = st.sidebar.selectbox("Rank of first group:", belts)
    gender_chosen_a = st.sidebar.selectbox("Gender of first group:", genders)
    
    st.sidebar.header("With:")
    belt_chosen_b = st.sidebar.selectbox("Rank of second group:", belts)
    gender_chosen_b = st.sidebar.selectbox("Gender of second group:", genders)


    def filter_data(data, belt_chosen, gender_chosen):
        
        if belt_chosen != belts[0]:
            data = data[data['current_belt'] == belt_chosen]
        
        data = data[data['current_belt'] != 'no answer']
            
        if gender_chosen != genders[0]:    
            data = data[data['gender'] == gender_chosen]
        
        data = data[data['gender'] != 'no answer']
        
        return data

    #data_subs = filter_data(data_subs, belt_chosen, gender_chosen)
    #colour = col_dictionary[belt_chosen]
    
else:   
    
    


colour = 'olivegreen'
    

# NORMALIZED STACKED BAR CHART 

def bar_plot(data_, column, count_):    

    data_bars = len(list(set(data_subs['technique'].to_list())))    
    
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
    
    st.altair_chart(bars)

st.subheader("Favourite submissions")    
bar_plot(data, 'current_belt', 'count(current_belt)') 
    
#data_reasons 
#data_least_f 
#data_podcast 
#data_web
#data_gi
#data_rash
#data_shorts 
#data_apparel 
#data_comp 
#data_injury 
#data_athlete 
#data_watch



# Q55: What is your gender?
# Q57: What is your age?
# Q59: What is your race/ethnicity?
# Q61: How would you describe yourself in terms of political ideology?
# Q67: Where is your nationality?
# Q56: What is your education level? Please select the highest degree you've completed.
# Q57.1: What is your income?
# Q22: How old were you when you started jiu jitsu?
# Q2: What is your current rank in jiu jitsu?
# Q3: How long have you been training jiu jitsu?
# Q6: How long did it take you to go from white belt to blue belt?
# Q7: How long did it take you to go from blue belt to purple belt?
# Q8: How long did it take you to go from purple belt to brown belt?
# Q9: How long did it take you to go from brown belt to black belt?
# Q10: On average, how many times do you train per week?
# Q11: Do you train both gi and no-gi?
# Q12: Do you prefer training gi or no-gi?
# Q66: To which academy do you belong? If it is affiliated, what is the affiliation? For instance:  Oceanside BJJ - A Royce Gracie Affiliate
# Q13: Does your academy focus on self-defense?
# Q27: Does your gym have a formal curriculum?
# Q66.1: Is your gym "leg lock friendly"?
# Q67.1: What is your preferred "style"?
# Q68: What is your favorite submission?
# Q14: What is your preferred time to train?
# Q16: Do you train at gyms when you travel?
# Q17: Did you have a background in another martial art before you started jiu jitsu?  If so, which one(s)?
# Q18: Why did you start training jiu jitsu?
# Q19: What is your favorite part about training?
# Q20: What is your least favorite part about training?
# Q23: Does your instructor encourage students at your gym to compete?
# Q24: Have you competed in jiu jitsu before?
# Q25: If you have competed, have you won any of the following medals?
# Q26: If you have competed, what was the organization (e.g., IBJJF, NAGA, etc.)? Fill in as many as apply!
# Q28: Have you had any serious injuries from doing jiu jitsu (that is, injuries that required weeks or months off or perhaps even surgery?) If so, please list the injuries and very briefly explain how they occurred and how long it took to recover--e.g., ACL tear via heel hook with 9 month recovery.
# Q30: Do you cross-train in other martial arts? If so, which one(s)?
# Q31: Do you do mobility exercises to prepare your body for jiu jitsu (e.g., ginastica natural)?
# Q32: Do you do yoga to prepare your body for jiu jitsu?
# Q60: Do you watch sport jiu jitsu?
# Q61.1: If you do watch sport jiu jitsu, what do you watch and where do you watch it? For instance, do you watch PPVs?  If so, which organizations--EBI, Metamoris, Polaris, etc.
# Q62: Do you have a favorite jiu jitsu athlete or athletes?
# Q63: Who are your favorite athletes (if any)? As always, leave this blank if it doesn't apply to you!
# Q33: How many gis do you own?
# Q39: What are some of your favorite gi manufactures?
# Q35: How many rash guards do you own?
# Q40: What are some of your favorite rash guard manufacturers?
# Q38: How many no-gi shorts do you own?
# Q41: What are some of your favorite short manufacturers?
# Q42: Do you buy jiu jitsu apparel (e.g., tee shirts, hats, etc.)?
# Q43: If you buy apparel, what are some of your favorite brands? If you don't buy apparel, leave blank!
# Q44: Have you ever had a problem with a particular manufacturer or brand?  If so, which one(s) and what was the problem?
# Q47: How much do you spend per year (on average) on gear and apparel?
# Q48: How much do you spend per month for membership dues?
# Q49: How much time do you spend per day (on average) reading or watching jiu jitsu-related material?
# Q50: If you have some favorite grappling-related websites and blogs, which ones do you like?
# Q65: If you have some favorite grappling-related podcasts, which ones do you like?















#'Q67.1':'preferred_style'
#data1 = filter_data(data, belt_chosen, gender_chosen)    
data1 = data 
    
st.subheader("Preferred style of fighting")

by_gr_dict = {'Current rank':['current_belt',belts[1:6]],
                 'Gender':['gender',None]}

def nomalised_barchart(data_, column, count_):
    
    data_ = data_[data_[column] != 'no answer']

    norm_bar = alt.Chart(data_).mark_bar().encode(
        y=alt.Y(by_gr_dict[by_group][0], title = by_group, 
                sort = by_gr_dict[by_group][1]),
                
        x=alt.X(count_, stack="normalize",
                title = 'Number of times mentioned',
                axis=alt.Axis(format='%')),
                
        color=column,
        tooltip = count_,
        order=alt.Order(column,sort = 'ascending')
        )

    st.altair_chart(norm_bar)
   
nomalised_barchart(data1, 'preferred_style','count(preferred_style)')    



##'Q66.1':'leg_lock_friendly',
#st.subheader("Is your gym leg-lock-friendly")
#
##'Q27':'gym_curriculum',    
#st.subheader("Does your gym have a formal curriculum")
#
##'Q13':'gym_self_defense',  
#st.subheader("Does your gym focus on self-defense")

#'Q56':'education',
#'Q55':'gender',
#'Q57':'age',
#'Q57.1':'income',
#'Q59':'race',
#'Q67':'nationality',

#'Q23':'instrutor_encourages_competition',
#'Q26':'comp_info',
#'Q48':'membership',

#'Q3':'training_years',
st.subheader("Number of training years")
nomalised_barchart(data1, 'training_years','count(training_years)')  


#'Q6':'white_blue',
#'Q7':'blue_purple',
#'Q8':'purple_brown',
#'Q9':'brown_black',


#'Q44':'Have you ever had a problem with a particular manufacturer or brand?',
#'Q18':'Why did you start training jiu jitsu?',
#'Q19':'What is your favorite part about training?',
#'Q20':'What is your least favorite part about training?',
#'Q61.1':'If you do watch sport jiu jitsu, what do you watch and where do you watch it?',
#'Q63':'Who are your favorite athletes (if any)?'




