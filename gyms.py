import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
from nltk.corpus import stopwords
from os import path

sw = stopwords.words("english")

#### My own python scripts from dictionary folder:

from Functions.functions import iterative_levenshtein as lev

path_w = r"C:\Users\kkql180\OneDrive - AZCollaboration\BJJ\BJJ_dataset"
path_h = r"C:\Users\malgo_000\Desktop\BJJ"

#%%
out_file = "unmatched.xlsx"

if path.isdir(path_w + '\BJJ1.csv'):
    path = path_w + r'\BJJ1.csv'
else:
    path = path_h + r'\BJJ1.csv'


#%%
# getting the data and deleting unimportant columns
data = pd.read_csv(path)        
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
#%%

def clean_sub(string):
    string= string.lower()
    list_replacements = [['&',','],['-',','],['/',','],['(',',']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9])|(\w+:\/\/\S+)'
    return ' '.join(re.sub(check, ' ', string).split())


###################  Academies ######################################

data_acedmy = data_q[["Q13","Q66","Q27","Q66.1"]]

def create_academy_list(dataset, columns):
    gi_list = []
    
    for col in columns:
        column = dataset[col][dataset[col] != ''].tolist()
        
        for row in column:
            gi_list += row.split(',')
    
    return [clean_sub(x) for x in gi_list if clean_sub(x) not in sw]
        

academy_list = create_academy_list(data_q, ["Q66"])

def most_frequent(List): 
    occurence_count = Counter(List)
    #print(occurence_count.most_common())
    return [x[0] for x in occurence_count.most_common()]

#%%
from Dictionaries.academy_dictionary import academy_dictionary
'''
academy_dict = {}
unsorted = most_frequent(academy_list)

for elem in unsorted[41:100]:
    print(elem)
    if elem not in academy_dict:
        academy_dict[elem] = [elem]
'''   



def leven_score(name, elem_list, min_ = 1):
    min_score = len(name)
    closest = ""
    
    for elem in elem_list:
        score = lev(elem, name)
        
        if score < min_score:
            min_score = score
            closest = elem
   
    return [name,closest,min_score] if len(name)>1 and len(closest)>1 else ''

new_academy_dictionary = academy_dictionary.copy()

#%%
gym_list_from_dict = [y for x in new_academy_dictionary.values() for y in x] 

def get_key(val): 
    for key, value in new_academy_dictionary.items(): 
         for elem in value:
             if val == elem: 
                 return key 

lista_do_sprawdzenia = list()
         
for academy in academy_list:
    closest = leven_score(academy, gym_list_from_dict)
 
    if len(closest) > 0:  
          
        if 0 < closest[2] < 4:
            print(closest)
    
            key = get_key(closest[1])
            #print("key: {}".format(key))
            
            if closest[0] not in new_academy_dictionary[key]:
                new_academy_dictionary[key].append(closest[0])
                print("'{}' --->  '{}' ---> '{}' ({})".format(closest[0],closest[1],key,closest[2]))
                
                if key not in new_academy_dictionary[key]:
                    new_academy_dictionary[key].append(key)
                    print('key was not in values for that key')
        
        elif 12 > closest[2] > 4:
            if closest[0] not in lista_do_sprawdzenia:
                #print("appended: '{}'".format(closest[0]))
                lista_do_sprawdzenia.append(closest[0])
        
        elif  closest[2] > 12:
            new_academy_dictionary[closest[0]] = [closest[0]]
            print("'{}' - added to the dictionary".format(closest[0]))
                 
#%%

with open(path_h + "\gym_dictionary.txt","w") as f:
    f.write('academy_dictionary = { \n')
    for key, value in sorted(new_academy_dictionary.items()):
        f.write("\'{}\':{},\n".format(key,value)) 
    f.write('}')
f.close()          
        
#%%
lista_do_sprawdzenia1 = []

for elem in lista_do_sprawdzenia:
    lista_do_sprawdzenia1.append(' '.join([x for x in elem.split(' ') if x not in sw ]))
 
 #%%
 
with open(path_h + r"\to_check_podcast.txt","w") as f:
    for row in sorted(lista_do_sprawdzenia1):
        f.write("'{}',\n".format(row))   
    f.close()    