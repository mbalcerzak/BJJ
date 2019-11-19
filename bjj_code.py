import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict



path = 'C:/Users/malgo_000/Desktop/BJJ/'

# getting the data and deleting unimportant columns
data = pd.read_csv(path + 'BJJ1.csv')
data = data.drop(columns = ['RecipientEmail','RecipientFirstName',
                            'RecipientLastName','IPAddress',
                            'ExternalReference', 'DistributionChannel'])
data = data.fillna('')
# creating a dictionaty for eventual future column names mapping
colnames = data[:][:1].values.tolist()[0]
colnames_dict = dict(zip(list(data), colnames))

# final dataset to be cleaned with questions only
qestions_order = sorted(list(data)[8:], key = lambda x: float(x[1:]))
data_q = data[qestions_order][2:]

######################## cleaning columns   ##########################

# freetext_variables = [18,19,20,26,28,39,40,41,43,50,61,63,65,66,67,68]

################## 1. Country Q67 --> "nationality"  #################

def generate_country_dict():
    country_dict = {
            'USA':['US','USA','States','American','america','Murrica','Murika',
                   'Murica','Virginia','Texan','Merica','Merican','Merkin'],
            'UK':['English','England','Scottish','Britain','British','Kingdom',
                  'Welsh','Scotland','UK'],
            'Netherlands':['NL','Dutch','Netherlands','Netherland',],
            'Ireland':['Irish','Ireland'],
            'Italy':['Italian','Italy'],
            'Germany':['German','Deutsch','getman','DE','Germany'],
            'Australia':['Australian', 'Austtalian','Australia'],
            'India':['Indian','India'],
            'Canada':['Canadian','Canada'],
            'Phillipines':['Filipino','Phillipines','Philippines'],
            'France':['French','France'],
            'Poland':['Polish','Poland'],
            'Japan':['Japanese','Okinawan','Japan'],
            'Brazil':['Brazilian','Brazillian', 'Brazil'],
            'Israel':['Israeli','Israel'],
            'Portugal':['Portuguese','Portugal'],
            'Iceland':['Icelandic','Iceland'],
            'Lithuania':['Lithuanian','Lithuania'],
            'Singapore':['Singaporean','Singapore'],
            'New Zealand':['NewZealander','NewZealand'],
            'Norway':['Norwegian','Norway'],
            'Colombia':['Colombian','Colombia'],
            'Vietnam':['Vietnamese','Vietnam'],
            'Denmark':['Danish','DK','Denmark'],
            'Sweden':['Swedish','Sweden'],
            'Uruguay':['Uruguayan','Uruguay'],
            'Pakistan':['Pakistani','Pakistan'],
            'Austria':['Austria','Austrian'],
            'Nicaragua':['Nicaragua'],
            'Russia':['Russian','Russia'],
            'China':['Chinese','China'],
            'Switzerland':['Swiss','Switzerland'],
            'Hungary':['Hungary','Hungarian'],
            'Serbia':['Serbian','serb','Serbia'],
            'Romania':['Romanian','Romania'],
            'Finland':['Finnish','Finland'],
            'Croatia':['Croatian','Croatia','cro'],
            'Bosnia':['Bosniak','Bosnian','Bosnia'],
            'South Africa':['SouthAfrican','SouthAfrica','SouthAfrican'],
            'Mexico':['Mexican','Mexico'],
            'Malaysia':['Malaysian','Malaysia'],
            'Greece':['Greek','Greece'],
            'South Korea':['Korean','Korea','SouthKorea'],
            'Egypt':['Egyptian','Egypt'],
            'Ecuador':['Ecuadorian','Ecuador'],
            'Spain':['Spanish','Spain'],
            'Czech Republic':['Czech'],
            'Ukraine':['Ukranian','Ukraine'],
            'Chile':['Chile'],
            'Turkey':['Turkish','Turkey'],
            'Indonesia':['Indonesia'],
            'Jamaica':['Jamaica'],
            'Cuba':['Cuban','Cuba'],
            'Macedonia':['Macedonian','Macedonia'],
            'Malta':['Maltese','Malta'],
            'Montenegro':['Montenegrin'],
            'Other':['Other']
            }
    
    country_dict2 = {}  
    for c_list, country in zip(list(country_dict.values()), country_dict.keys()):
        for c in c_list:
            country_dict2[c.lower()] = country
    
    return country_dict2

country_dict = generate_country_dict()


def clean_text(string):
    string= string.lower()
    list_replacements = [['.',''],['new ','new'],['south ','south']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z]+)|([^A-Za-z \t\&])|(\w+:\/\/\S+)'
    return (' '.join(re.sub(check, ' ', string).split())).split(' ')

data_q['country_list'] = [clean_text(x) for x in data_q['Q67']]

def country_get(word_list):
    nationalities = []
    
    for word in word_list:
        nationality = ''
        if word.lower() in country_dict.keys():
            nationality = country_dict[word.lower()]
        if nationality != '' and nationality not in nationalities:
            nationalities.append(nationality)      
        if nationality == 'Other':
            break
    
    return nationalities
        
data_q['nationality'] = [country_get(x) for x in data_q['country_list']] 
  

################## Q57 - age ##################

age_data = data['Q57'][data['Q57'] != '']
data['age_data'] = age_data[2:].apply(int) 

def age_categories(x):    
    return '{}-{}'.format(int(x//5*5),int(x//5*5+5)) if x == x else ''
    
data['age_category'] = data['age_data'][2:].apply(age_categories)  


# Overall, do not split into belts or gender:
# [57, 59, 67, 56, 57.1, 22]


############### [18,19,20,28],  Wordcloud ##############



#[39,40,41, 43] Gi i NoGi ulubione ciuchy

#[13,66, 27,66.1] Academies

#61.1 watching sport BJJ


#26 competition
# 28 most popular injuries

# 50, 65 blogs and podcasts

# let's leave a question about politics...

# 63,68]

# 68 favourite submission

# 63 favourite athletes

