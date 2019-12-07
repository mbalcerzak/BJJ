import pandas as pd
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


from Dictionaries.submissions_dictionary import submissions_dictionary 
from Functions.functions import assign_dict_keys
from Functions.functions import clean_string


list_replacements = [['\'',''],[' & ','&']]
check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t\&])|(\w+:\/\/\S+)'

#%%

data_q['Q68_clean'] = data_q['Q68'].apply(lambda x: clean_string(x, list_replacements,check))

data_q['submissions_found'] = data_q['Q68_clean'].apply(lambda x: assign_dict_keys(submissions_dictionary,x))

data_sub = data_q[['submissions_found','Q68_clean']]