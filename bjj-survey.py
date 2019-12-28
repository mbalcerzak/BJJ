import streamlit as st
import pandas as pd
from Functions.for_streamlit.bygroups_app import bygroups_show
from Functions.for_streamlit.overall_app import overall_show
from Dictionaries.colnames_dictionary import header_dictionary as hd

st.title('BJJ  Survey Results')

DATA_URL = ('https://raw.githubusercontent.com/mbalcerzak/BJJ/master/Data')

#@st.cache
# ---------------------- LOADING DATA FROM GITHUB -------------------------- #
def load_data(file_name):
    data = pd.read_csv(DATA_URL + '/{}.csv'.format(file_name), sep = ';')

    if 'training' in file_name:
        for column in ["how_old_when_started", "num_gis", "num_rashguards", 
                       "num_shorts"]:    
        
            def chop(x):
                return str(x[1:-1]) if x != 'no answer' else x
            
            data[column] = data[column].apply(lambda x: chop(x))
    
    return data

data_load_state = st.text('Loading data...')

data_view = load_data("data_bjj") # the one that has a pre-view

data = load_data("info/training_info")
data_back_ma = load_data("info/background_info")
data_current_ma = load_data("info/current_ma_info")
data_subs = load_data("info/subs_info")
data_reasons = load_data("info/reasons_info")
data_least_f = load_data("info/least_f_info")
data_podcast = load_data("info/podcast_info")
data_web = load_data("info/web_info")
data_gi = load_data("info/gi_info")
data_rash = load_data("info/rash_info")
data_shorts = load_data("info/shorts_info")
data_apparel = load_data("info/apparel_info")
data_comp = load_data("info/comp_info")
data_injury = load_data("info/injury_info")
data_athlete = load_data("info/athlete_info")
data_watch = load_data("info/watch_info")


data_load_state.text('Loading data... done!')

# ----------------- FINISHED LOADING DATA FROM GITHUB ---------------------- #

st.sidebar.text("github.com/mbalcerzak")

st.sidebar.header("Overall results or for a selected group?")

all_or_not = st.sidebar.selectbox("",["Overall",
                                  'Show by groups',
                                  'Select one group',
                                  'Interesting raw data'])

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

genders = ['Every gender', 'Male', 'Female']

    return data[data[column] != 'no answer']

if all_or_not == 'Show by groups':
    
    by_group = 'Current rank'
    
    st.sidebar.header("Split the answers by ...")
    by_group = st.sidebar.radio("",['Current rank','Gender'])

    by_gr_dict = {'Current rank':['current_belt', belts[1:6]],
                  'Gender':['gender', None]}  
    
    
    data1 = only_answers(by_gr_dict[by_group][0], data)
    data_back_ma1 = only_answers(by_gr_dict[by_group][0], data_back_ma)
    data_current_ma1 = only_answers(by_gr_dict[by_group][0], data_current_ma)

    bygroups_show(data1, data_back_ma1, data_current_ma1, by_gr_dict, by_group)


elif all_or_not == 'Select one group':
    
    by_belt = False
    by_gender = False
    
    belt_chosen = belts[0]
    gender_chosen = genders[0]
    
    belt_chosen = st.sidebar.selectbox("Rank of the group:", belts)
    gender_chosen = st.sidebar.selectbox("Gender of the group:", genders)
    
    colour = col_dictionary[belt_chosen]
    
    def filter_data(data, belt_chosen = belt_chosen,
                    gender_chosen = gender_chosen):

        if belt_chosen != belts[0]:
            data = data[data['current_belt'] == belt_chosen]
        
        data = data[data['current_belt'] != 'no answer']
            
        if gender_chosen != genders[0]:    
            data = data[data['gender'] == gender_chosen]
        
        data = data[data['gender'] != 'no answer']
        
        return data
    
    if belt_chosen != belts[0] or gender_chosen != genders[0]:
        
        data_f = filter_data(data)
        data_current_ma_f = filter_data(data_current_ma)
        data_back_ma_f = filter_data(data_back_ma)
        data_reasons_f = filter_data(data_reasons)
        data_least_f_f = filter_data(data_least_f)
        data_subs_f = filter_data(data_subs)
        data_podcast_f = filter_data(data_podcast)
        data_web_f = filter_data(data_web)
        data_gi_f = filter_data(data_gi)
        data_rash_f = filter_data(data_rash)
        data_shorts_f = filter_data(data_shorts)
        data_apparel_f = filter_data(data_apparel)
        data_comp_f = filter_data(data_comp)
        data_injury_f = filter_data(data_injury)
        data_athlete_f = filter_data(data_athlete)
        data_watch_f = filter_data(data_watch) 
        
        if belt_chosen != belts[0]:
            by_belt = True
        
        if gender_chosen != genders[0]:
            by_gender = True
    
        overall_show(data_f, data_current_ma_f, data_back_ma_f, data_reasons_f, 
                     data_least_f_f, data_subs_f, data_podcast_f, data_web_f, 
                     data_gi_f, data_rash_f, data_shorts_f, data_apparel_f, 
                     data_comp_f, data_injury_f, data_athlete_f, data_watch_f, 
                     colour, by_gender, by_belt, selected = True)


elif all_or_not == 'Interesting raw data':
    data_raw = load_data("data_raw")
    
    def only_answers_col(column, data = data_raw):
        return data[column][data[column] != 'no answer']
    
    st.subheader(hd['Q18'])
    if st.checkbox('Show answers:'):        
        st.table(only_answers_col('reasons_raw'))
    
    st.subheader(hd['Q19'])
    if st.checkbox('Show answers:'):
        st.table(only_answers_col('favourite_raw'))
    
    st.subheader(hd['Q20'])
    if st.checkbox('Show answers:'):
        st.table(only_answers_col('least_fav_raw'))
    
    st.subheader(hd['Q44'])
    if st.checkbox('Show answers:'):
        st.table(only_answers_col('brand_problem'))


else:   
    
    if st.checkbox('Show the data used for analysis'):
        st.subheader('Answers')
        st.write(data_view)
        
    colour = 'steelblue'
    
    #st.sidebar.radio("",['royalblue','midnightblue','navy','steelblue'])

    overall_show(data, data_current_ma, data_back_ma, data_reasons, 
                 data_least_f, data_subs, data_podcast, data_web, data_gi, 
                 data_rash, data_shorts, data_apparel, data_comp, data_injury, 
                 data_athlete, data_watch, colour, by_gender = False, 
                 by_belt= False, selected = False)
    