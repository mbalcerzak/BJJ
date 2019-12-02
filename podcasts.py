import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
from nltk.corpus import stopwords
sw = stopwords.words("english")

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

data_media = data_q[["Q50","Q61.1","Q65", "Q63"]]

def clean_sub2(string):
    string= string.lower()
    list_replacements = [['\'',''],[' & ','&']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t\&/\.])|(\w+:\/\/\S+)'
    return ' '.join(re.sub(check, ' ', string).split())

def create_academy_list(dataset, columns):
    gi_list = []
    
    for col in columns:
        column = dataset[col][dataset[col] != ''].tolist()
        
        for row in column:
            gi_list += row.split(',')
    
    return [clean_sub2(x) for x in gi_list if clean_sub(x) not in sw]
        

media_list = create_academy_list(data_q,["Q50","Q61.1","Q65", "Q63"])


media_dict = {
         '10th planet':['10th planet','10thplanet'],
         'reddit':['r/','reddit'],
         'budo':['budo'],
         'adcc': ['adcc'],
         'youtube': ['youtube','you tube'],
         '40plusbjjsuccess': ['40plusbjjsuccess'],
         'ebi': ['ebi'],
         'bjj scout': ['bjj scout', 'bjjscout'],
         'bjj eastern europe': ['bjj eastern europe','bjj ee', 'bjj easter europe','bjj eastern eirope','bjjee','eastern eu','eebjj','bjjeastern', 'bjjeasteneurope'],
         'bjj geek': ['bjj geek'],
         'bjj news': ['bjj news','bjjnews'],
         'bjj globtrotters': ['bjj globtrotters'],
         'live matches': ['live matches'],
         'ibjjf': ['ibjjf','ibjff'],
         'bjjscandinavia': ['bjjscandinavia'],
         'jiujitsutimes': ['jiujitsutimes', 'jiujutsu times','jiujitsu times','jiu jitsu time','jujitsutimes'],
         'bjjnews': ['bjjnews'],
         'xande ribeiro': ['xande'],
         'the grumpy grappler': ['the grumpy grappler'],
         'sherdog': ['sherdog'],
         'savagekitsune': ['savagekitsune'],
         'sharkgirlbjj': ['sharkgirlbjj'],
         'tristargym': ['tristargym'],
         'lexfridman': ['lexfridman'],
         'chewjitsu': ['chewjitsu'],
         'grapplearts': ['grapplearts'],
         'pro jitsu': ['pro jitsu'],
         'polaris': ['polaris'],
         'subf15teen': ['subf15teen'],
         'flo grappling': ['flo grappling'],
         'metamoris': ['metamoris','mentamoris','meramoris'],
         'ainec': ['ainec'],
         'mma mania': ['mma mania'],
         'bjj brick': ['bjj brick','bjjbrick'],
         'mixedmartialarts': ['mixedmartialarts'],
         'fight to win':['fight to win','fight 2 win','fight2win'],
         'meerkatsu blog': ['meerkatsu blog'],
         'flo grapplimg': ['flo grapplimg','flograpplimg'],
         'flow grappling': ['flow grappling','flowgrappling', 'flo'],
         'mma junkie': ['mma junkie'],
         'bloody elbow': ['bloody elbow'],
         'ppv':['ppv'],
         'live':['live'],
        'fightpass':['fightpass'],
        'white belt bjj':['white belt'],
        'maxbjj':['maxbjj'],
        'bjj library':['bjjlibrary', 'bjj library'],
        'jiu jitsu style': ['jiu jitsu style'],
         'grapplers guide': ['grapplers guide','grapplersguide'],
         'instagram': ['instagram'],
         'inverted gear': ['inverted gear'],
         'insidebjj': ['insidebjj'],
         'otm':['otm'],
         'friends compete':['teammate','friend'],
         'grappling central':['grappling central', 'grapplingcentral'],
         'bjj over 40':['bjj over 40']
        }
