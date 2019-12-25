import re
import pandas as pd

#######################  ITERATIVE LEVENSHTEIN ##############################
#
#   compuing the distance between two strings
#   discovering how similar those strings are
#
##############################################################################

def iterative_levenshtein(s, t):

    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    for i in range(1, rows):
        dist[i][0] = i

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

##################  GETTING THE KEY FROM THE VALUE ###########################
#
#   finding a key from the selected dictionary using this key's value
#
##############################################################################

def get_key(val,dictionary): 
    for key, value in dictionary.items(): 
         for elem in value:
             elem = elem.lower()
             if val == elem: 
                 return key 

########################  USING THE DICTIONARY ###############################
#
#   after getting all the values into dictionaries it's  time to assign them
#
##############################################################################
    
def assign_dict_keys(dictionary, string):
    
    def find_dictionary_vals(string):
        string = str(string).lower()
        result = []
        
        if string != '':
            for row in dictionary.values():
                for elem in row:
                    elem = elem.lower()
                    if elem in string:
                        key_val = get_key(elem,dictionary)
                        if key_val not in result:
                            result.append(key_val)   
    
        if len(result) == 0:
            result = ['no answer']
    
        return result
    
    return find_dictionary_vals(string)

#########################  CLEAN COLUMN VALUES ###############################
#
#   after getting all the values into dictionaries it's  time to assign them
#
##############################################################################

def clean_string(string, list_replacements, check):
    
    string= string.lower()

    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])
    
    string = ' '.join(re.sub(check, ' ', string).split())
    
    return string if string == string else ''

######################### CLEAN COLUMN VALUES ################################
#
#   after getting all the values into dictionaries it's time to assign them
#   and get a correctly classified answer
#
##############################################################################

def dictionary_processing(data, chosen_columns, check, list_replacements, 
                          dictionary, new_names = []):   

    data_ = data[chosen_columns].copy()

    for column in chosen_columns:
        data_[column + '_clean'] = data_[column] \
            .apply(lambda x: clean_string(x, list_replacements,check))
        data_[column + '_list'] = data_[column + '_clean'] \
            .apply(lambda x: assign_dict_keys(dictionary,x))
    
    leave_cols = [x for x in list(data_) if '_list' in x]
    
    data_ = data_[leave_cols]
    if len(new_names) > 0:
        data_.columns = new_names
    
    return data_

#################### find values without clearning the column ################

def find_dict_vals(string,dictionary):
    dict_vals = [x for y in dictionary.values() for x in y]
    string = string.lower()
    result = []
    
    for val in dict_vals:
        if val in string:
            key = get_key(val,dictionary)
            if key not in result:
                result.append(key)
    
    if len(result) == 0:
        result = ['no answer']
    
    return result

####################  split list into new rows ###############################
    
def explode(dataset, variable, new_var_name, na = True):
    country_list_ = list(dataset)
    country_list_.remove(variable)
  
    dataset[variable] = dataset[variable].apply(lambda x: str(x[1:-1]).split(','))
    
    dataset_ = (dataset
              .set_index(country_list_)[variable]
              .apply(pd.Series)
              .stack()
              .reset_index()
              .rename(columns={0:new_var_name}))
       
    if na == False:
        dataset_ = dataset_[dataset_[new_var_name] != 'NA']
    
    return dataset_[[x for x in list(dataset_) if 'level' not in x]]

#################  choke / not a choke #######################################
    
def is_choke(x):
    if x == ['no answer'] or len(x) == 0:
        return 'no answer'
    
    word_list = ['choke', 'triangle', 'bow & arrow', 'guillotine', 'ezekiel',
                 'darce', 'gogoplata','crucifix', 'anaconda', 'papercutter',
                 'sorcerer', 'single wing']
    
    for word in word_list:
        for elem in x:
            if word in elem:
                return 'Yes'
        
    return 'No'

####################### age cathegories ######################################
    
def age_categories(x):   
    if x != 'no answer':
        return '{}-{}'.format(round(int(x)//5*5), round(int(x)//5*5+5))
    else:
        return x