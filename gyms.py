import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
from nltk.corpus import stopwords
sw = stopwords.words("english")

#### My own python scripts from dictionary folder:

from Dictionaries.country_dictionary import country_dict

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


academy_dict = {
        
        '10th planet':['10th planet'],
        'alliance':['alliance'],
        'capital mma':['capital mma','capitol takoma','capital mm'],
        'chapel hill':['chapel hill'],
        'carlson gracie':['carlson gracie'],
        'devine':['devine'],
        'gracie barra':['gracie barra'],
        'next generation':['next generation'],
        'renzo gracie':['renzo gracie'],
        'royce gracie':['royce gracie','royce affiliate'],
        'roger gracie':['roger gracie'],
        'roger machado':['roger machado'],
        'checkmat':['checkmat'],
        
        
        }

