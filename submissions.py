import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
from nltk.corpus import stopwords
from os import path 

sw = stopwords.words("english")

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

######################## cleaning columns   ##########################

# freetext_variables = [18,19,20,26,28,39,40,41,43,50,61,63,65,66,67,68]


#26 competition
# let's leave a question about politics...
# add number of answers taken into account for each quesion


# 68 favourite submission

submission_dictionary = {
         'triangle':['triangle'],
         'kimura':['kimura','kimora','kamra','kmrr'] ,
         'armbar':['armbar', 'arm bar', 'armbars','arm entanglement','juji gatame'],
         'bow and arrow':['arrow'],
         'americana':['americana','anericana','key lock'],
         'rear naked choke':['rear naked choke','rnc','rear naked'],
         'omoplata':['omoplata','omaplata','omo plata','omplata'],
         'guillotine':['guillotine','guilotine'],
         'heel hook':['heel hook'],
         'ezekiel':['ezekiel','ezkiel','ezikiel'],
         'cross collar choke':['cross','cros side','collar'],
         'darce':['darce'],
         'ankle lock':['ankle'],
         'gogoplata':['gogoplata','gogo plata'],
         'crucifix':['crucifix'],
         'wristlock':['wrist'],
         'anaconda':['anaconda'],
         'leg lock':['leg lock','texas clover leaf'],
         'armlock':['armlock','arm lock'],
         'brabo choke':['brabo'],
         'head and arm choke':['head and arm','head&arm','kata gatame','katagatami'],
         'baseball choke':['baseball choke'],
         'foot lock':['foot lock'],
         'toe hold':['toe hold','toehold'],
         'twister':['twister'],
         'peruvian necktie':['north south','paruvian','n s choke'],
         'japanese necktie / papercutter':['japanese necktie','paper cutter','papercutter'],
         'lapel chokes':['lapel chokes'],
         'sorcerer':['sorceror'],
         'kneebar':['kneebar','knee bar'],
         'clock choke':['clock choke'],
         'electric chair':['electric chair'],
         'loop choke':['loop choke'],
         'calf slicer':['calf slicer'],
         'gi choke':['gi chokes','gi choke'],
         'sambo leg knot':['russian knee knot'],
         'rickson choke':['rickson choke'],
         'single wing':['kata hajime single wing'],
         'bread cutter choke':['bread cutter'],
         'choke from back':['choke from back']
        }

choke_words = ['choke','chokin','chocke','cuck']

def clean_sub(string):
    string= string.lower()
    list_replacements = [['\'',''],[' & ','&']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t\&])|(\w+:\/\/\S+)'
    return ' '.join(re.sub(check, ' ', string).split())

def create_submissions(column):
    sub_list = column[column != ''].tolist()
    
    return [clean_sub(row) for row in sub_list]
    
 
sub_list2 = create_submissions(data_q['Q68'])