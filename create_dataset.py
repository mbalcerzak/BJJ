import pandas as pd
from os import path
from nltk.corpus import stopwords
sw = stopwords.words("english")
from Functions.functions import dictionary_processing

path_w = r"C:\Users\kkql180\OneDrive - AZCollaboration\BJJ\BJJ_dataset"
path_h = r"C:\Users\malgo_000\Desktop\BJJ"

if path.isdir(path_w + '\BJJ1.csv'):
    path = path_w + r'\BJJ1.csv'
else:
    path = path_h + r'\BJJ1.csv'
 
############################################################################## 
# getting the data and deleting unimportant columns
data = pd.read_csv(path)
data = data.drop(columns = ['RecipientEmail','RecipientFirstName',
                            'RecipientLastName','IPAddress',
                            'ExternalReference', 'DistributionChannel'])

data = data.fillna('no answer')

# creating a dictionaty for future column names mapping
colnames = data[:][:1].values.tolist()[0]
colnames_dict = dict(zip(list(data), colnames))

# final dataset with questions only
qestions_order = sorted(list(data)[8:], key = lambda x: float(x[1:]))
data_q = data[qestions_order][2:]

########################## age categories ####################################
from Functions.functions import age_categories
    
data_q['age_cat'] = data_q['Q57'].apply(age_categories)  

############ corrected case so it's consistent with other values #############

data_q['Q2'][data_q['Q2'] == 'White belt'] = 'White Belt' 

######################### rename columns #####################################

data_q.rename({
        'Q55':'gender',
        'Q2':'belt'
        }, axis=1, inplace=True)        

##########################  nationality  #####################################

from Dictionaries.country_dictionary import country_dictionary
from Functions.functions import explode

data_dem = dictionary_processing(
               data = data_q, 
               chosen_columns = ['Q67'],
               check = '(@[A-Za-z]+)|([^A-Za-z \t\&])|(\w+:\/\/\S+)',
               list_replacements = [['.',''],['new ','new'], \
                                    ['south ','south']], 
               dictionary = country_dictionary,
               new_names = ['countries'])
  
data_q = data_q.join(data_dem[['countries']])
data_q = explode(data_q, 'countries', 'country')

#%%  #######################  athletes  ######################################

from Dictionaries.athlete_dictionary import athlete_dictionary 

data_athletes = dictionary_processing(
               data = data_q, 
               chosen_columns = ['Q63'],
               check = '(@[A-Za-z]+)|([^A-Za-z])|(\w+:\/\/\S+)',
               list_replacements = [['\'s',''],['.',','],['/',','],\
                                    [' and ',','],['&',','],[';',','], \
                                    ['!',','],['-',',']], 
               dictionary = athlete_dictionary,
               new_names = ['athletes'])

#%%  #####################  submissions  #####################################

from Dictionaries.submissions_dictionary import submissions_dictionary 

data_submissions = dictionary_processing(
                       data = data_q, 
                       chosen_columns = ['Q68'],
                       check = \
                          '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t\&])|(\w+:\/\/\S+)',
                       list_replacements = [['\'',''],[' & ','&']], 
                       dictionary = submissions_dictionary,
                       new_names = ['submissions'])

#%%
from Functions.functions import is_choke

data_submissions['choke'] = data_submissions['submissions'].apply(lambda x: is_choke(x))

#%%

#def pie_chart_generator(data,question):
#    question_list = data[question][data[question] != '']
#    
#    counts = Counter(question_list[2:].tolist())
#    plt.pie([int(v) for v in counts.values()], labels=[str(k) for k in counts.keys()],
#             autopct='%.1f%%')
#    plt.show()

# pie_chart_generator(data_submissions2,'technique')

#%% ##################   Gi & NoGi favourite brands  #########################

from Dictionaries.gi_dictionary import gi_dictionary

data_gi = dictionary_processing(
                data = data_q,         
                chosen_columns = ["Q39","Q40","Q41","Q43"],
                check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t\&])|(\w+:\/\/\S+)',
                list_replacements = [['\'',''],[' & ','&']], 
                dictionary = gi_dictionary,
                new_names = ['gi','rash','shorts','apparel'])

#data_gi2 = explode(data_gi, 'Q68_list', 'technique', na = False)

#%% ############## BJJ academies and affiliations ############################

from Dictionaries.academy_dictionary import academy_dictionary

data_gyms = dictionary_processing(
                data = data_q, 
                chosen_columns = ["Q66"] ,
                check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9])|(\w+:\/\/\S+)',
                list_replacements = [['&',','],['-',','],['/',','],['(',',']], 
                dictionary = academy_dictionary,
                new_names = ['gym'])

#%% ##################   Podcasts / YT channels ...  #########################

from Dictionaries.media_dictionary import media_dictionary

data_podcasts = dictionary_processing(
                data = data_q, 
                chosen_columns = ["Q50","Q61.1","Q65"] ,
                check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t/])|(\w+:\/\/\S+)',
                list_replacements = [['\'',''],[' & ',','],['www.',','], \
                                     [' and ',','],['. ',','],['.com',',']], 
                dictionary = media_dictionary,
                new_names = ['website','watch_sport','podcast'])

#%% ###########################   injuries  ##################################

from Dictionaries.injuries_dictionary import injuries_dictionary

data_injuries = dictionary_processing(
                data = data_q, 
                chosen_columns = ["Q28"] ,
                check = '(@[A-Za-z]+)|([^A-Za-z])|(\w+:\/\/\S+)',
                list_replacements = [['\'s','']], 
                dictionary = injuries_dictionary,
                new_names = ['injuries'])

#%% ########################   organisations  ################################

from Dictionaries.organisation_dictionary import organisation_dictionary

data_org = dictionary_processing(
                data = data_q, 
                chosen_columns = ["Q26"] ,
                check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9])|(\w+:\/\/\S+)',
                list_replacements = [['\'s',''],['-',' ']], 
                dictionary = organisation_dictionary,
                new_names = ['organisations'])  

#%%#################### reasons why you started #############################

from Dictionaries.reasons_dictionary import reasons_dictionary
from Functions.functions import find_dict_vals

data_q['reasons'] = data_q['Q18'].apply(lambda x: find_dict_vals(x,reasons_dictionary))

#data_reasons = data_q[['reasons']].join(data_q[['Q18']])

#%% ################# least favourite thing about BJJ #######################

from Dictionaries.least_fav_dictionary import least_fav_dictionary

data_q['favourite'] = data_q['Q20'].apply(lambda x: find_dict_vals(x,least_fav_dictionary))

#data_fav = data_q[['favourite']].join(data_q[['Q20']])
#%%
list_datasets = [data_athletes,data_submissions,data_gi,data_gyms,data_podcasts,data_injuries,data_org]

for dataset in list_datasets:
    data_q = data_q.join(dataset)