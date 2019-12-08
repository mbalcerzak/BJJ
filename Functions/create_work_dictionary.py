from nltk.corpus import stopwords
sw = stopwords.words("english")

from Functions.functions import iterative_levenshtein as lev
from Functions.functions import get_key

#################### FUNCTION TO CREATE A DICTIONARY #########################
#
#   I am creating a work-in-progress dictionary, where I find words similar
#   to  values in a selected dictionary (Dictionary directory)
#
#   For example:
#    1. Existing dictionary:
#        
#        athletes_dictionary = {
#                'keenan cornelious':['keenan cornelious']
#                }
#
#   2. Someone entered 'keenan kornelious' into the survey
#
#   3. Using Levenshtein distance I calulate the score: 1
#
#   4. If it's less than X (declared in the function) I am adding it to the     
#      appropriate key in the dictionary 
#
#   5. If the values are too different from any existing value I can create a
#      new key
#
#   6. I am running the algorithm until each value from the survey is assigned
#
##############################################################################
#
#   out_path = where do you want the created file to be saved
#
#   dictionary = an accepted previous dictionary (base)
#
#   input_list = values to be found in the dictionary and checked with 
#                Levenshtein distance
#
##############################################################################

def create_work_dictionary(out_path, dictionary, input_list):
    
    def leven_score(name, elem_list, min_ = 1):
        min_sc = len(name)
        closest = ""
        
        for elem in elem_list:
            score = lev(elem, name)
            
            if score < min_sc:
                min_sc = score
                closest = elem
       
        return [name,closest,min_sc] if len(name)>1 and len(closest)>1 else ''
    
    # ------------------------------------------------------------------------
    new_dictionary = dictionary.copy()
    values_from_new_dict = [y for x in new_dictionary.values() for y in x] 
    list_to_check = list()
        
    # ------------------------------------------------------------------------     
    for element in input_list:
        closest = leven_score(element, values_from_new_dict)
     
        if len(closest) > 0:  
              
            if 0 < closest[2] < 4:
                print("\n")
        
                key = get_key(closest[1],new_dictionary)
                print("key: {}".format(key))
                
                if closest[0] not in new_dictionary[key]:
                    new_dictionary[key].append(closest[0])
                    print("'{}' --->  '{}' ---> '{}' ({})" \
                          .format(closest[0],closest[1],key,closest[2]))
                    
                    # I want each key also in the values
                    if key not in new_dictionary[key]:
                        new_dictionary[key].append(key)
                        print('KEY itself was not in values. Added it')
            
            elif 12 > closest[2] > 4:
                if closest[0] not in list_to_check:
                    print("appended: '{}'".format(closest[0]))
                    list_to_check.append(closest[0])
            
            elif  closest[2] > 12:
                new_dictionary[closest[0]] = [closest[0]]
                print("'{}' - added to the dictionary".format(closest[0]))
                     
    # ------------------------------------------------------------------------            
    with open(out_path + "\dictionary_to_check.txt","w") as f:
        f.write('dictionary = { \n')
        for key, value in sorted(new_dictionary.items()):
            f.write("\'{}\':{},\n".format(key,value)) 
        f.write('}')
    f.close()          
    
    print('{}_to_check.txt created!'.format(dictionary))        
    
    # ------------------------------------------------------------------------
    list_to_check_final = []
    
    for element in list_to_check:
        list_to_check_final \
            .append(' '.join([x for x in element.split(' ') if x not in sw ]))
       
    with open(out_path + r"\list_to_check.txt","w") as f:
        for row in sorted(list_to_check_final):
            f.write("'{}',\n".format(row))   
        f.close()  
    
    
    return 'list_to_check.txt created!'