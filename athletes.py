import pandas as pd
import re
from collections import Counter
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

from Dictionaries.athlete_dictionary import athlete_dict

athlete_dict = athlete_dict

stop_words = ['act','almost','also','always','amazing','anybody','anyone',
              'appreciation','basically','beautiful','beer','best','big','bjj',
              'california','classic','cool','deep','doses','etc','ever','everyone',
              'exciting','fan','fascinates','favourites','fight','friend','fun',
              'game','got','greats','gui','guys','heart','high','instructional',
              'instructors','interesting','keeps','kid','killing','knowledge',
              'level','like','list','lived','lot','love','made','man','many',
              'master','materials','may','mg','mma','monsters','mr','name','nerd',
              'ones','others','outrageous','partners','passing','peeps','peers',
              'personality','play','plays','pounds','quality','quite','really',
              'reason','right','say','sexy','small','sport','style','stylistically',
              'successful','switch','teammates','think','trained','training','try',
              'ufc','various','vegas','watch','watching','women','world','yeah',
              'year','years']

sw += stop_words

#%%
def most_frequent(List): 
    occurence_count = Counter(List)
    #print(occurence_count.most_common())
    return [x[0] for x in occurence_count.most_common()]

athletes_list = data_q["Q63"].tolist()

#%%  stuff to replace
to_replace = {'marcelo garcia eddie Bravo':'marcelo garcia/ eddie Bravo',
              'Tammi Musumeci Michelle Nicolini ':'Tammi Musumeci /Michelle Nicolini ',
              'Bernardo Faria  Rodolfo Vieira Marcelo Garcia':'Bernardo Faria / Rodolfo Vieira/ Marcelo Garcia',
              'Keenan clark estimas xandre gerry tonnon':'Keenan/ clark/ estimas/ xandre/ gerry tonnon',
              'Roger Gracie Michelle nicollini Gary Tonon':'Roger Gracie/ Michelle nicollini/ Gary Tonon',
              'Xande roger saulo micheal leria kron Michelle nicollne Caio erra':'Xande/ roger/ saulo/ micheal leria/ kron/ Michelle nicollne/ Caio erra',
              'Jeff glover Gary tonon':'Jeff glover/ Gary tonon',
              'Kron gracie Marcelo garcia Eddie cummings Rafael mendes Garry tonon':'Kron gracie/ Marcelo garcia/ Eddie cummings/ Rafael mendes/ Garry tonon',
              'Kron gracie rodolfo Viera Luiz heredia ':'Kron gracie/ rodolfo Viera/ Luiz heredia ',
              'Daniel Beleza Guybson Sa':'Daniel Beleza/ Guybson Sa',
              'Brags Neto ,Ralph, Reno Ryan Gordo  Nino ':'Brags Neto ,Ralph, Reno, Ryan Gordo,  Nino ',
              'BJ Penn Jacarae':'BJ Penn/ Jacarae',
              'Roger is amazing keeps it classic. I lived in LA for 3 years and trained with Ryron Gracie. The knowledge is outrageous. Best personality ever. I may be 200 pounds but I try to act and play like Jeff Glover and the reason I got into the sport is BJ Penn AND The California Kid Urijah Faber':'Roger, Ryron Gracie, Jeff Glover, BJ Penn, Urijah Faber'}

new_athlete_list = []

for elem in athletes_list:
    
    if elem in to_replace:
        new_athlete_list.append(to_replace[elem])
       # print("{} : {}".format(elem,to_replace[elem]))
    else:
        new_athlete_list.append(elem)

#%%

def clean_sub3(string):
    string= string.lower()
    list_replacements = [['\'s','']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z]+)|([^A-Za-z])|(\w+:\/\/\S+)'
    
    string =  re.sub(check, ' ', string).strip()
    
    return ' '.join([x for x in string.split(' ') if x not in sw])



athletes = []


for row in new_athlete_list:

    clean_row = row.replace('.',',').replace('/',',').replace(' and ',',').replace('&',',').replace(';',',').replace('!',',').replace('-',',')
    clean_row = clean_row.strip()
    athletes += [clean_sub3(x).strip() for x in clean_row.split(',') if x != '']

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
athletes_values_list = []

for row in list(athlete_dict.values()):
    for elem in row:
        elem = elem.strip()
        athletes_values_list += [' '.join([x for x in elem.split(' ') if x not in sw])]
    
#%%
def leven_score(name):

    min_ = len(name)
    closest = ""
    
    for athlete in athletes_values_list:
        if iterative_levenshtein(athlete, name) < min_:
            min_ = iterative_levenshtein(athlete, name)
            closest = athlete
            
    return [name,closest,min_] if min_ > 1 else ''

unmatched_athletes = []
        
for athlete in athletes:
    if len(athlete) > 0:
        x = leven_score(athlete)
        if len(x) > 0: unmatched_athletes.append(x)

#%%
with pd.ExcelWriter(path_h + '\\' + out_file) as writer:
    
    df = pd.DataFrame(unmatched_athletes)
    df.columns = ["Athlete", "Closest", "Min"]
    df.to_excel(writer)
    
    workbook = writer.book
    format = workbook.add_format({'text_wrap': True})	
    
    writer.sheets['Sheet1'].set_column("B:B",75, format)	
    writer.sheets['Sheet1'].set_column("C:C",40, format)	
    
writer.save()
writer.close() 

#%%
'''
for key, value in sorted(new_gi_dict.items()):
    print("\'{}\':{},".format(key,value))
    
    

#%%

lista_do_dict = []

dict_ = {}

for elem in lista_do_dict:
    print("\'{}\':[\'{}\'],".format(elem.title(),elem))
'''