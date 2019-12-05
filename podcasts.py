import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
from nltk.corpus import stopwords
sw = stopwords.words("english")

from Functions.functions import iterative_levenshtein as lev

path_w = r"C:\Users\kkql180\OneDrive - AZCollaboration\BJJ\BJJ_dataset"
path_h = r"C:\Users\malgo_000\Desktop\BJJ"

#%%
out_file = "unmatched.xlsx"

while True:
    try:
        path = path_h + '\BJJ1.csv'
        break
    except FileNotFoundError:
        pass
    else:
        path = path_w + '\BJJ1.csv'
        break

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

#  65 blogs and podcasts

data_media = data_q[["Q50","Q61.1","Q65"]]

stop_words = [
        'wings','anything','also','watch','whatever','eveything','anything','preference',
        'really','none','dont','favourite','http','com','none', 'etc','none','non',
        'sometimes','havent', 'found', 'one', 'doesnt', 'seem', 'like',
        'previously', 'followed','main', 'excellent','slightly','related',
        'ive', 'tried','watched','difficult','forgot','etc','n/a','find'] + sw

def clean_sub(string):
    string= string.lower()
    list_replacements = [['\'',''],[' & ',','],['www.',','],[' and ',','],['. ',','],['.com',',']]

    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t/])|(\w+:\/\/\S+)'
    
    result = ' '.join(re.sub(check, ' ', string).split())

    return ' '.join([x for x in result.split(' ') if x not in stop_words])

def create_academy_list(dataset, columns):
    gi_list = []
    
    for col in columns:
        column = dataset[col][dataset[col] != ''].tolist()
        
        for row in column:
            gi_list += row.split(',')
    
    return [clean_sub(x) for x in gi_list if clean_sub(x)]
        

media_list = create_academy_list(data_q,["Q50","Q61.1","Q65"])

media_list = [x for x in media_list if x]
#%%
from Dictionaries.media_dictionary import media_dictionary

media_list_from_dict = [y for x in media_dictionary.values() for y in x] 
new_media_dict = {}

#%%
def leven_score(name, elem_list, min_ = 1):
    min_score = len(name)
    closest = ""
    
    for elem in elem_list:
        score = lev(elem, name)
        
        if score < min_score:
            min_score = score
            closest = elem
   
    return [name,closest,min_score] if len(name)>1 and len(closest)>1 else ''

new_media_dictionary = media_dictionary

#%%


#%% 
def get_key(val): 
    for key, value in new_media_dictionary.items(): 
         for elem in value:
             if val == elem: 
                 return key 
 
lista_do_sprawdzenia = list()
         
for podcast in media_list:
    closest = leven_score(podcast, media_list_from_dict)
 
    if len(closest) > 0:        
        if closest[2] in [1,2]:
            #print(closest)
    
            key = get_key(closest[1])
            #print("key: {}".format(key))
            
            if closest[0] not in new_media_dictionary[key]:
                new_media_dictionary[key].append(closest[0])
                print("'{}' --->  '{}' ---> '{}'".format(closest[0],closest[1],key))
        
        elif closest[2] > 0:
            if closest[0] not in lista_do_sprawdzenia:
                #print("appended: '{}'".format(closest[0]))
                lista_do_sprawdzenia.append(closest[0])
     

#%%            
with open(path_w + r"\media_dictionary.txt","w") as f:
    f.write('media_dictionary = { \n')
    for key, value in sorted(new_media_dictionary.items()):
        f.write("\'{}\':{},\n".format(key,value)) 
    f.write('}')
f.close()    

 #%%
lista_do_sprawdzenia1 = []

for elem in lista_do_sprawdzenia:
    lista_do_sprawdzenia1.append(' '.join([x for x in elem.split(' ') if x not in sw ]))
 
 #%%
 
with open(path_w + r"\to_check_podcast.txt","w") as f:
    for row in sorted(lista_do_sprawdzenia1):
        f.write("'{}',\n".format(row))   
    f.close()             
#%%
    
list1 =[
]    

for elem in list1:
    print("\'{}\':[\'{}\'],".format(elem, elem))
    
    