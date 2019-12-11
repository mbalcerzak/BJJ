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

#%%


#%%  why started and favourite thing

reasons = data['Q18'][2:].to_list()

favourite = data['Q19'][2:].to_list()

from collections import Counter 


own_sw = ['wanted','want','year','really','getting']
check = '(@[A-Za-z]+)|([^A-Za-z])|(\w+:\/\/\S+)'
list_replacements = [['no answer','']]

favourite_list = [clean_string(x) for x in favourite]
reasons_list = [clean_string(x) for x in reasons]
#%%

def print_most_common(megalist): 
    Counter_ = Counter(megalist) 
    most_occur = Counter_.most_common() 

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
                
                s = sorted(row[n:n + num])
                
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

reasons_single = coocuring_most_common(reasons_list,1)
reasons_single =[x for x in reasons_single if x != '']

#%%
reasons_double = coocuring_most_common(reasons_list,2)
reasons_triple = coocuring_most_common(reasons_list,3)

#%%

print_most_common(reasons_single,10)
print_most_common(reasons_double,10)
print_most_common(reasons_triple,10)

#%%

favourive_single = coocuring_most_common(favourite_list,1)
favourive_double = coocuring_most_common(favourite_list,2)
favourive_triple = coocuring_most_common(favourite_list,3)

#%%

print_most_common(favourive_single,10)
print_most_common(favourive_double,10)
print_most_common(favourive_triple,10)

#%%
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
from PIL import Image

# Create some sample text
text = ' '.join(favourive_single)

image_path = r"C:\Users\malgo_000\Desktop\belt_colours2.png"

alice_coloring = np.array(Image.open(image_path))
stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(background_color="white", max_words=600, mask=alice_coloring,
               stopwords=stopwords, max_font_size=150, random_state=42)

wc.generate(text)

image_colors = ImageColorGenerator(alice_coloring)

plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")

plt.show()

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

injuries = data['Q28'][2:].tolist()
injuries1 = [clean_sub3(x).strip() for x in injuries if x != 'no answer']
injuries2 = ' '.join(injuries1).split()

#%%
to_check = most_frequent(injuries)

#%%
stopwords = ['months','weeks','recovery','month','broken','tear','training','torn','via','took','surgery','injury','week','injuries','dislocated','takedown','time','guard','sprained','back',
 'still',
 'two',
 'right',
 'got',
 'one',
 'nothing',
 'pain',
 'year',
 'rolling',
 'popped',
 'sprain',
 'due',
 'serious',
 'separated',
 'left',
 'three',
 'strain',
 'mat',
 'bjj']


from Dictionaries.injuries_dictionary import injuries_dictionary

dict_values = [x for y in injuries_dictionary.values() for x in y]


to_check = [x for x in to_check if x not in dict_values + stopwords]

m_t_chec = most_frequent(to_check)

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
            
    return [name,closest,min_] if min_ > 1 else ''

unmatched_athletes = []
        
for athlete in injuries2:
    if len(athlete) > 0:
        x = leven_score(athlete)
        if len(x) > 0: unmatched_athletes.append(x)


#%%
  
    
    
lista_do_dict = [

 ]

dict_ = {}

for elem in lista_do_dict:
    print("\'{}\':[\'{}\'],".format(elem,elem))
     
        
#%%        
        
for key, value in sorted(new_gi_dict.items()):
    print("\'{}\':{},".format(key,value))     
    
    

