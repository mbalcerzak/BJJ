import re

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


########################  USING THE DICTIONARY ###############################
#
#   after getting all the values into dictionaries it's  time to assign them
#
##############################################################################
    
def assign_dict_keys(dictionary, string):

    def get_key(val): 
        for key, value in dictionary.items(): 
             for elem in value:
                 if val == elem: 
                     return key 
    
    def find_dictionary_vals(string):
        string = str(string).lower()
        result = []
        
        if string != '':
            for row in dictionary.values():
                for elem in row:
                    elem = elem.lower()
                    if elem in string:
                        key_val = get_key(elem)
                        if key_val not in result:
                            result.append(key_val)   
    
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

    return ' '.join(re.sub(check, ' ', string).split())