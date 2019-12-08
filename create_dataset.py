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
data = data.fillna('')

# creating a dictionaty for future column names mapping
colnames = data[:][:1].values.tolist()[0]
colnames_dict = dict(zip(list(data), colnames))

# final dataset with questions only
qestions_order = sorted(list(data)[8:], key = lambda x: float(x[1:]))
data_q = data[qestions_order][2:]

########################## age categories ####################################

def age_categories(x):   
    if x == x and x != '':
        return '{}-{}'.format(round(int(x)//5*5),round(int(x)//5*5+5))
    
data_q['age_cat'] = data_q['Q57'].apply(age_categories)  

#%% ######################  nationality  #####################################

from Dictionaries.country_dictionary import country_dictionary

data_dem = dictionary_processing(
               data = data_q, 
               chosen_columns = ['Q67'],
               check = '(@[A-Za-z]+)|([^A-Za-z \t\&])|(\w+:\/\/\S+)',
               list_replacements = [['.',''],['new ','new'], \
                                    ['south ','south']], 
               dictionary = country_dictionary,
               to_keep = ['Q55','Q2'])

data_dem.rename({
        'Q67_list':'countries', 
        'Q55':'gender',
        'Q2':'belt'
        }, axis=1, inplace=True)

# corrected case so it's consistent with other values   
data_dem['belt'][data_dem['belt'] == 'White belt'] = 'White Belt' 

data_q = data_q.join(data_dem)

#%%  #######################  athletes  ######################################

from Dictionaries.athlete_dictionary import athlete_dictionary 

data_athletes = dictionary_processing(
               data = data_q, 
               chosen_columns = ['Q63'],
               check = '(@[A-Za-z]+)|([^A-Za-z])|(\w+:\/\/\S+)',
               list_replacements = [['\'s',''],['.',','],['/',','],\
                                    [' and ',','],['&',','],[';',','], \
                                    ['!',','],['-',',']], 
               dictionary = athlete_dictionary)
 
#%%  #####################  submissions  #####################################

from Dictionaries.submissions_dictionary import submissions_dictionary 

data_submissions = dictionary_processing(
                       data = data_q, 
                       chosen_columns = ['Q68'],
                       check = \
                          '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t\&])|(\w+:\/\/\S+)',
                       list_replacements = [['\'',''],[' & ','&']], 
                       dictionary = submissions_dictionary)

#%% ##################   Gi & NoGi favourite brands  #########################

from Dictionaries.gi_dictionary import gi_dictionary

data_gi = dictionary_processing(
                data = data_q,         
                chosen_columns = ["Q39","Q40","Q41","Q43"],
                check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t\&])|(\w+:\/\/\S+)',
                list_replacements = [['\'',''],[' & ','&']], 
                dictionary = gi_dictionary)

#%% ############## BJJ academies and affiliations ############################

from Dictionaries.academy_dictionary import academy_dictionary

data_gyms = dictionary_processing(
                data = data_q, 
                chosen_columns = ["Q66"] ,
                check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9])|(\w+:\/\/\S+)',
                list_replacements = [['&',','],['-',','],['/',','],['(',',']], 
                dictionary = academy_dictionary)

#%% ##################   Podcasts / YT channels ...  #########################

from Dictionaries.media_dictionary import media_dictionary

data_podcasts = dictionary_processing(
                data = data_q, 
                chosen_columns = ["Q50","Q61.1","Q65"] ,
                check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t/])|(\w+:\/\/\S+)',
                list_replacements = [['\'',''],[' & ',','],['www.',','], \
                                     [' and ',','],['. ',','],['.com',',']], 
                dictionary = media_dictionary)
