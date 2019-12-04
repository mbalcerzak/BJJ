import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
from nltk.corpus import stopwords
sw = stopwords.words("english")

#### My own python scripts from dictionary folder:


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


def clean_sub(string):
    string= string.lower()
    list_replacements = [['\'',''],[' & ','&']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t\&])|(\w+:\/\/\S+)'
    return ' '.join(re.sub(check, ' ', string).split())


##################   Gi i NoGi ulubione ciuchy  #########################

data_gi = data_q[["Q39","Q40","Q41","Q43"]]

def create_gi_company_list(dataset, columns):
    gi_list = []
    
    for col in columns:
        column = dataset[col][dataset[col] != ''].tolist()
        
        for row in column:
            row = row.replace('and',',').replace('(',',').replace('/',',').replace('.',',')
            gi_list += row.split(',')
    
    return [clean_sub(x) for x in gi_list if clean_sub(x) not in sw]
        
gi_list = create_gi_company_list(data_q, ["Q39","Q40","Q41","Q43"])
gi_list = [x.strip() for x in gi_list if x != '']
  
#%% 
from Dictionaries.gi_dictionary import gi_dictionary
gi_list_from_dict = [y for x in gi_dictionary.values() for y in x] 
new_gi_dict = {}
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

new_gi_dict = gi_dictionary

#%%

stop_words = ['wings','anything','aslso',
              'really','none','dont','favourite','http','com','none'] + sw

#%% 
def get_key(val): 
    for key, value in new_gi_dict.items(): 
         for elem in value:
             if val == elem: 
                 return key 
 
lista_do_sprawdzenia = list()
         
for gi in gi_list:
    closest = leven_score(gi, gi_list_from_dict)
 
    if len(closest) > 0:        
        if closest[2] in [1,2]:
            print(closest)
    
            key = get_key(closest[1])
            #print("key: {}".format(key))
            
            if closest[0] not in new_gi_dict[key] + stop_words:
                #new_gi_dict[key].append(closest[0])
                print("'{}' --->  '{}' ---> '{}'".format(closest[0],closest[1],key))
        
        elif closest[2] > 0:
            if closest[0] not in lista_do_sprawdzenia:
                #print("appended: '{}'".format(closest[0]))
                lista_do_sprawdzenia.append(closest[0])
     


#%%            
with open(r"C:\Users\malgo_000\Desktop\BJJ\gi_dictionary.txt","w") as f:
    f.write('gi_dictionary = { \n')
    for key, value in sorted(new_gi_dict.items()):
        f.write("\'{}\':{},\n".format(key,value)) 
    f.write('}')
f.close()        

# =============================================================================
# #%%
# 
# new_gi_list_from_dict = ' '.join([y for x in new_gi_dict.values() for y in x]).split(' ')
# lista_do_sprawdzenia2 = ' '.join(lista_do_sprawdzenia).split(' ')
# 
# #%%
# 
# to_check_manually = [x for x in lista_do_sprawdzenia2 if x not in new_gi_list_from_dict + sw]
# to_check = list(set(to_check_manually))
# 
# #%%
# lista_do_sprawdzenia1 = []
# for elem in lista_do_sprawdzenia:
#     lista_do_sprawdzenia1.append(' '.join([x for x in elem.split(' ') if x not in sw]))
# 
# #%%
# 
# with open(r"C:\Users\malgo_000\Desktop\BJJ\to_check_gi.txt","w") as f:
#     for row in sorted(lista_do_sprawdzenia1):
#         f.write("{},\n".format(row))   
# f.close()             
# 
# 
# #%%
# 
# 
# with open(r"C:\Users\malgo_000\Desktop\BJJ\to_check_gi.txt","w") as f:
#     for row in lista_do_sprawdzenia:
#         f.write("{},\n".format(row))   
# f.close() 
# =============================================================================

