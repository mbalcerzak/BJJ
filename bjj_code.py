import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict



#path = 'C:/Users/malgo_000/Desktop/BJJ/'
path = r"C:\Users\kkql180\OneDrive - AZCollaboration\BJJ\BJJ_dataset"


# getting the data and deleting unimportant columns
data = pd.read_csv(path + '\BJJ1.csv')
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

def age_categories(x):   
    if x == x and x != '':
        return '{}-{}'.format(round(int(x)//5*5),round(int(x)//5*5+5))
    
data_q['age_category'] = data_q['Q57'].apply(age_categories)  

##### Overall, do not split into belts or gender:
data_all = data_q[["Q57", "Q55", "age_category", "nationality", "Q59", "Q56", "Q57.1", "Q22"]]

############### [18,19,20,28],  Wordcloud ##############




# Gi i NoGi ulubione ciuchy

data_gi = data_q[["Q39","Q40","Q41", "Q43"]]

# Academies

data_acedmy = data_q[["Q13","Q66","Q27","Q66.1"]]


#26 competition
# let's leave a question about politics...
# add number of answers taken into account for each quesion

#  65 blogs and podcasts

data_media = data_q[["Q50","Q61.1","Q65", "Q63"]]


# 68 favourite submission

submission_dictionary = {
         'triangle':['triangle'],
         'kimura':['kimura','kimora','kamra','kmrr'] ,
         'armbar':['armbar', 'armbars','arm entanglement'],
         'bow and arrow':['arrow'],
         'americana':['americana','anericana'],
         'rear naked choke':['rear naked choke','rnc','rear naked'],
         'armbar':['arm bar', 'armbar'],
         'omoplata':['omoplata','omaplata','omo plata','omplata'],
         'guillotine':['guillotine','guilotine'],
         'heel hook':['heel hook'],
         'ezekiel':['ezekiel','ezkiel','ezikiel'],
         'cross collar choke':['cross','cros side','collar'],
         'darce':['darce'],
         'ankle lock':['ankle'],
         'heel hook':['heel hook'],
         'gogoplata':['gogoplata','gogo plata'],
         'crucifix':['crucifix'],
         'wristlock':['wristlock','wrist lock'],
         'anaconda':['anaconda'],
         'leg lock':['leg lock','texas clover leaf'],
         'armlock':['armlock','arm lock','armlocks'],
         'brabo choke':['brabo'],
         'head and arm choke':['head and arm','head&arm','kata gatame','katagatami'],
         'baseball choke':['baseball choke'],
         'foot lock':['foot lock'],
         'toe hold':['toe hold','toehold'],
         'twister':['twister'],
         'peruvian necktie':['north south','paruvian','n s choke'],
         'japanese necktie / papercutter':['japanese necktie','paper cutter','papercutter'],
         'lapel chokes':['lapel chokes'],
         'sorcerer':['sorceror']
        }

 'loop choke', 'choke','chokes', 'knee bar'
 'kneebar' ,  , 'electric chair',
 'front choke', 
 'chokes any',  'gi chokes', 
 'abc always be chokin',   , ,
  'cuck', 'calf slicer', 'rickson choke', 
 , 'juji gatame', , 'choke from back',
   , 'russian knee knot' 'clock choke', 'any choke',  'chocke',
  'bread cutter choke',   'key lock', 'best friend choke triangle', 
 'kata hajime single wing choke', 'gi choke'

submission_list = data_q['Q68'][data_q['Q68'] != ''].tolist()


def clean_sub(string):
    string= string.lower()
    list_replacements = [['\''',''],[' & ','&']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z]+)|([^A-Za-z \t\&])|(\w+:\/\/\S+)'
    return ' '.join(re.sub(check, ' ', string).split())


def create_submissions():
    sub_list = []
    
    for row in submission_list:
        sub_list.append(clean_sub(row))
        
    return sub_list
    
sub_list2 = create_submissions()
    
    
def most_frequent(List): 
    occurence_count = Counter(List) 
    return [x[0] for x in occurence_count.most_common()]
    
print(most_frequent(sub_list2))     
    
    
    
    