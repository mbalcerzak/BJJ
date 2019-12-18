import pandas as pd
from os import path 
from nltk.corpus import stopwords
sw = stopwords.words("english")
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import re
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

#%%  why started and favourite thing

from Functions.functions import clean_string 

reasons = data['Q18'][2:].tolist()

favourite = data['Q19'][2:].tolist()

least = data['Q20'][2:].tolist()

injuries = data['Q28'][2:].tolist()

organisation = data['Q26'][2:].tolist()

from collections import Counter 

# Fitness and intrigue.
# I wanted to be a Ninja
# To leg lock my enemies 
# my room mate in college would by me beer if I went with him
# At this point in my life, partially for self-defense, but mostly to have 
# something to do. Martial arts in general is one of those perfect hobbies: 
#    it's cheap and it is simultaneously a mental, physical, social, and 
#    spiritual endeavor. BJJ is also one of the most challenging things 
#    I've dealt with in my life in all of those aspects as well. In short, 
#    it improves the quality of my life.
# Because the boxing coach looked really dodgy and the jiujitsu crew were much better organised, as well as better looking.
# Exercise without feeling like exercise. 
# I lost a fight to a jiu jitsu guy.
# I saw a video of Ottavia Bourdain climbing an ice cream shop owner like a tree and choking him to the ground.  This led me down a youtube rabbit hole and I thought, gosh that looks like fun!
# I saw that I could get a good workout while lying on soft mats.
# I was always into wrestling with my cousins and siblings, so my mom signed me up for my first Jiu-Jitsu class so I could learn how to do it properly.
# after this guy slept with my boyfriend and i needed to fuck people up


def clean_string1(string, list_replacements, check):
    
    #string= string.lower()

    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])
    
    string = ' '.join(re.sub(check, ' ', string).split())
    
    return string if string == string else ''


own_sw = ['wanted','want','year','really','getting']
check = '(@[A-Z]+)|([^A-Z])|(\w+:\/\/\S+)'
list_replacements = [['no answer','']]

org_list = [clean_string1(x,list_replacements,check) for x in organisation]

#%%
from Dictionaries.injuries_dictionary import injuries_dictionary 

def print_most_common(megalist,n): 
    Counter_ = Counter(megalist) 
    most_occur = Counter_.most_common(n) 

    return most_occur  

def coocuring_most_common(lista, num):
    wordlist = []
    
    if num == 1:
        for row in lista:
            wordlist += row.split(' ')
    else:
        for row in lista:
            row = row.split(' ')
            for n in range(len(row)-num+1):
                
                s = row[n:n + num]
                
                # I am cheking if the words are unique so that I don't end up
                # with CT_CT_CT ...
                
                if len(s) == 3:
                    if s[0] != s[1] != s[2]:
                        wordlist.append('_'.join(s))
                        
                elif len(s) == 2:
                    if s[0] != s[1]:
                        wordlist.append('_'.join(s))
                else:
                    wordlist.append('_'.join(s))
                #wordlist.append('_'.join(row[n:n + num]))
            
    return wordlist

#%%

reasons_single = coocuring_most_common(org_list,1)
reasons_single =[x for x in reasons_single if x != '' and x not in sw]

#%%
reasons_double = coocuring_most_common(org_list,2)
reasons_triple = coocuring_most_common(org_list,3)

#%%

print_most_common(reasons_single,30)

#%%
print_most_common(reasons_double,30)

#%%
print_most_common(reasons_triple,30)

#%%

def most_frequent(List): 
    occurence_count = Counter(List)
    # print(occurence_count.most_common())
    # occurence_count.most_common()
    return [x[0] for x in occurence_count.most_common()]

def clean_sub3(string):
    string= string.lower()
    list_replacements = [['\'s','']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z]+)|([^A-Za-z])|(\w+:\/\/\S+)'
    
    string =  re.sub(check, ' ', string).strip()
    
    return ' '.join([x for x in string.split(' ') if x not in sw])

#'Q26':'competition_organisaiton'

injuries = data['Q26'][2:].tolist()
injuries1 = [clean_sub3(x).strip() for x in injuries if x != 'no answer']
injuries2 = ' '.join(injuries1).split()

#%%
to_check = most_frequent(injuries1)

#%%
stopwords = ['months','weeks','recovery','month','broken','tear','training','torn',
             'via','took','surgery','injury','week','injuries','dislocated','takedown'
             ,'time','guard','sprained','still','two','right','got','one',
             'pain','year','rolling','popped','sprain','due','serious','separated',
             'left','three','strain','mat','bjj'
 ]


from Dictionaries.injuries_dictionary import injuries_dictionary

dict_values = [x for y in injuries_dictionary.values() for x in y]


to_check = [x for x in to_check if x not in dict_values] #+ stopwords]

m_t_chec = most_frequent(to_check)

new_injuries_dictionary = injuries_dictionary

#%%
def iterative_levenshtein(s, t):

    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings 
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                 dist[row][col-1] + 1,      # insertion
                                 dist[row-1][col-1] + cost) # substitution

    return dist[row][col]

#%%
#athletes_values_list = []

#for row in list(injuries_dictionary.values()):
#    for elem in row:
#        elem = elem.strip()
#        athletes_values_list += [' '.join([x for x in elem.split(' ') if x not in sw])]
#    
#%%
  


def leven_score(name):

    min_ = len(name)
    closest = ""
    
    for athlete in dict_values:
        if iterative_levenshtein(athlete, name) < min_:
            min_ = iterative_levenshtein(athlete, name)
            closest = athlete
     
        
        
    return [name,closest,min_] if min_ > 0 else ''

unmatched_athletes = []
        
for athlete in injuries2:
    if len(athlete) > 0:
        x = leven_score(athlete)
        if len(x) > 0: unmatched_athletes.append(x)



#%%
  
lista_do_dict = []

dict_ = {}

for elem in lista_do_dict:
    print("\'{}\':[\'{}\'],".format(elem,elem))
     
        
#%%        
from Dictionaries.organisation_dictionary import organisation_dictionary    
#for key in qestions_order:
#    print("\'{}\':\'{}\',".format(key,colnames_dict[key]))     

#for key in sorted(organisation_dictionary.keys()):
#    print("\'{}\':{},".format(key,organisation_dictionary[key]))     
#   

#%% - -------------------------------------------------------------------
    

    
values = [x for y in organisation_dictionary.values() for x in y]
    
cols = 'Q26'

reasons_df = data[[cols]][2:].copy()

reasons_df = reasons_df[reasons_df[cols] != 'no answer']

reasons_df[cols] = [x.lower() for x in reasons_df[cols]]

def get_key(val,dictionary): 
    for key, value in dictionary.items(): 
         for elem in value:
             elem = elem.lower()
             if val == elem: 
                 return key   

def find_dict_vals(string):
    result = []
    for val in values:
        if val in string:
            key = get_key(val,organisation_dictionary)
            if key not in result:
                result.append(key)
    return result

reasons_df['reasons'] = reasons_df[cols].apply(lambda x: find_dict_vals(x))

resons_not_found = reasons_df[reasons_df['reasons'].str.len() == 0]

#%%
#
#
#lista_do_dict = resons_not_found['Q26'].to_list()
#
#dict_ = {}
#
#for elem in lista_do_dict:
#    print("\'{}\':[\'{}\'],".format(elem,elem))
     