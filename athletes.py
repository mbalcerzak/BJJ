import pandas as pd
import re
from collections import Counter
from nltk.corpus import stopwords
sw = stopwords.words("english")

#%%
out_file = "unmatched.xlsx"

while True:
    try:
        path = r"C:\Users\malgo_000\Desktop\BJJ\BJJ1.csv"
    except FileNotFoundError:
        pass
    else:
        path = r"C:\Users\kkql180\OneDrive - AZCollaboration\BJJ\BJJ_dataset\BJJ1.csv"
        print("dataset loaded")
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

athlete_dict = {
'Adam Benayoun':['adam benayoun'],
'AJ Azagarm':['aj azagarm'],
'Alexandre "Soca" Freitas':['alexandre "soca" freitas'],
'Aloisio Silva':['aloisio silva'],
'Alvaro Barreto':['alvaro barreto'],
'André Galvão':['andré galvão','andre galvao','galvao'],
'Armando Wridt':['armando wridt'],
'Arthur Virgílio Neto':['arthur virgílio neto'],
'B.J. Penn':['b.j. penn','bj penn'],
'Bernardo Faria':['bernardo faria'],
'Braulio Estima':['braulio estima','braulio'],
'Bruno Malfacine':['bruno malfacine','malfacine'],
'Brian Ortega':['brian ortega'],
'Carley Gracie':['carley gracie'],
'Carlos "Bagana" Lima':['carlos "bagana" lima'],
'Carlos "Caique" Elias':['carlos "caique" elias'],
'Carlos Antonio Rosado':['carlos antonio rosado'],
'Carlos Gracie':['carlos gracie'],
'Carlos Gracie, Jr.':['carlos gracie, jr.'],
'Carlos Machado':['carlos machado'],
'Carlos Valente':['carlos valente'],
'Rolando Samson':['rolando samson'],
'Carlson Gracie':['carlson gracie'],
'Charles Gracie':['charles gracie'],
'Chris Haueter':['chris haueter'],
'Clark Gracie':['clark gracie'],
'Lucas Leite':['lucas leite'],
'Danaher Death Squad':['danaher death squad','danaher group'],
'Dean Lister':['dean lister','lister'],
'Demian Maia':['demian maia','damien maia'],
'Derval Luciano Rêgo (Mestre Morcego)':['derval luciano rêgo (mestre morcego)'],
'Eddie Bravo':['eddie bravo'],
'Eddie Cummings':['eddie cummings', 'eddie cummins', 'cummings'],
'Fabio Gurgel':['fabio gurgel'],
'Fabricio Martins Costa':['fabricio martins costa'],
'Fabrício Werdum':['fabrício werdum'],
'Flavio Behring':['flavio behring'],
'Francisco Mansor':['francisco mansor'],
'Francisco Sá (Sazinho)':['francisco sá (sazinho)'],
'Fábio Santos (fighter)':['fábio santos (fighter)'],
'Gastão Gracie':['gastão gracie'],
'Garry Tonon':['garry tonon','tonon','gary tonon'],
'Geny Rebello':['geny rebello'],
'Gezary Matuda':['gezary matuda'],
'Gilbert Burns':['gilbert burns'],
'Glover Teixeira':['glover teixeira'],
'Gordon Ryan':['gordon ryan'],
'Hélio Gracie':['hélio gracie'],
'Helvecino Penna':['helvecio penna'],
'Jean Jacques Machado':['jean jacques machado'],
'Jeff Glover':['jeff glover'],
'Joaquim Valente':['joaquim valente'],
'Joe Moreira':['joe moreira'],
'Joe Rogan':['joe rogan'],
'John Danaher':['john danaher', 'danaher'],
'Jorge (George) Gracie':['jorge (george) gracie'],
'Jorge Pereira':['jorge pereira'],
'João Alberto Barreto':['joão alberto barreto'],
'Keenan Cornelius':['keenan cornelious', 'keenan'],
#'kennnan kornelius', 'keenan cornelius', 'keenan cornielius', 'keenan kornelius', 'kennen cornelius'],
'Ken Gabrielson':['ken gabrielson'],
'Kenny Florian':['kenny florian'],
'Kron Gracie':['kron gracie', 'kron'],
'Kurt Osiander':['kurt osiander', 'ocieander', 'oisander', 'kurt osiander'],
'Luis Carlos Guedes de Castro':['luis carlos guedes de castro'],
'Luis Franca':['luis franca'],
'Luiz França Filho':['luiz frança filho'],
'Luiz Fux':['luiz fux'],
'Luiz Palhares':['luiz palhares'],
'Leandro Lo':['leandro lo'],
'Léo Vieira':['léo vieira'],
'Mackenzie Dern':['mackenzie dern', 'mckenzie dern', 'meckenzie dern', 'makinzie dern'],
'Marcelo Garcia':['marcelo garcia','marcello garcia','marcelo'],
'Marcus "Buchecha" Almeida':['marcus "buchecha" almeida','marcus buchecha almeida'],
'Marcus Buchecha':['buchecha'],
'Marcus Soares':['marcus soares'],
'Mauricio Motta Gomes':['mauricio motta gomes'],
'Mendes Bros':['mendez', 'mendes', 'mendes bros', 'mendes brothers'],
'Michael Langhi':['michael langhi'],
'Michelle Nicollini':['michelle nicolini'],
'Mickey Gall':['mickey gall'],
'Milton Vieira':['milton vieira'],
'Miyao Brothers':['miao bros', 'miyao', 'miyao brothers'],
'Moises Muradi':['moises muradi'],
'Murilo Bustamante':['murilo bustamante'],
'Márcio Stambowsky':['márcio stambowsky'],
'Nate Diaz':['nate diaz'],
'Nelson Monteiro':['nelson monteiro'],
'Nick Diaz':['nick diaz'],
'Osvaldo Alves':['osvaldo alves'],
'Oswaldo Fadda':['oswaldo fadda'],
'Oswaldo Gracie':['oswaldo gracie'],
'Pablo Popovitch':['pablo popovitch'],
'Patrice Poissant':['patrice poissant'],
'Pedro Diaz':['pedro diaz'],
'Pedro Hemeterio':['pedro hemeterio'],
'Pedro Sauer':['pedro sauer'],
'Pedro Valente Sr.':['pedro valente sr.'],
'Rafael Lovato Jr.':['rafael lovato jr.','rafael lovato'],
'Rafael Mendes':['rafael mendes','rafa mendes','rafa'],
'Relson Gracie':['relson gracie'],
'Renato Paquet':['renato paquet'],
'Rener Gracie':['rener gracie'],
'Renzo Gracie':['renzo gracie'],
'Reyson Gracie':['reyson gracie'],
'Ricardo De La Riva':['ricardo de la riva'],
'Ricardo Murgel':['ricardo murgel'],
'Ricardo Vieira':['ricardo vieira'],
'Rickson Gracie':['rickson gracie', 'ricks on gracie','rickson'],
'Rigan Machado':['rigan machado'],
'Rilion Gracie':['rilion gracie'],
'Roberto "Cyborg" Abreu':['roberto "cyborg" abreu','cyborg'],
'Robson Gracie (Carlos Robson Gracie)':['robson gracie (carlos robson gracie)'],
'Robson Moura':['robson moura'],
'Rodolfo Vieira':['rodolfo vieira', 'rodolpho'],
                  #viera', 'rodalfo vierrea', 'rodoflo viera', 'rodolfo', 'rodolfo vieira', 'rodolfo viera','rodalfo vierrea','rodolpho viera'],
'Roger Gracie':['roger gracie','roger'],
'Romulo Barral':['romulo barral'],
'Rhadi Ferguson':['rhadi ferguson'],
'Rolker Gracie':['rolker gracie'],
'Rolls Gracie':['rolls gracie'],
'Romero "Jacare" Cavalcanti':['romero "jacare" cavalcanti'],
'Ronaldo "Jacare" Souza':['ronaldo souza','jacare souza','ronaldo jacare'],
'Rorion Gracie':['rorion gracie'],
'Roy Dean':['roy dean'],
'Royce Gracie':['royce gracie'],
'Royler Gracie':['royler gracie','royler'],
'Rubens "Cobrinha" Charles':['rubens "cobrinha" charles',"cobrinha"],
'Ryan Hall':['ryan hall'],
'Ryron Gracie':['ryron gracie'],
'Saulo Ribeiro':['saulo ribeiro','saulo ribero'],
'Sergio "Malibu" Jardim':['sergio "malibu" jardim'],
'Shamil Gamzatov':['shamil gamzatov'],
'Stephan Kesting':['stephan kesting'],
'Sylvio Behring':['sylvio behring'],
'Sérgio Penha':['sérgio penha'],
'Tom Barlow':['tom barlow'],
'Vinny Magalhães':['vinny magalhães'],
'Vitor Ribeiro':['vitor ribeiro'],
'Wellington "Megaton" Dias':['wellington "megaton" dias'],
'Wilson Mattos':['wilson mattos'],
'Xande Ribeiro':['xande ribeiro','xande','xande ribiero'],
'Yvonne Duarte':['yvonne duarte'],
'Yuri Simoes':['yuri simoes','i ve recently become a fan of yuri simoes'],
'Edwin Najmi':['edwin najmi'],
'Gabriel Arges':['gabriel arges'],
 }


def most_frequent(List): 
    occurence_count = Counter(List)
    #print(occurence_count.most_common())
    return [x[0] for x in occurence_count.most_common()]

althetes_list = data_q["Q63"].tolist()


def clean_sub3(string):
    string= string.lower()
    list_replacements = [['\'s','']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z]+)|([^A-Za-z])|(\w+:\/\/\S+)'
    
    return re.sub(check, ' ', string).strip()

athletes = []
for row in althetes_list:
    athletes += [clean_sub3(x) for x in row.replace('.',',').replace('/',',').replace(' and ',',').split(',') if x != '']



check = '(@[A-Za-z]+)|([^A-Za-z])|(\w+:\/\/\S+)'

althletes_megastring = ''.join([re.sub(check,'',x).lower() for x in athletes])

#%%
def iterative_levenshtein(s, t):
    """ 
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings 
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein 
        distance between the first i characters of s and the 
        first j characters of t
    """
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

for elem in list(athlete_dict.values()):
    athletes_values_list += elem


def leven_score(name):
    
    '''
    New idea for checking:
        if 2 words - check for 2 words,
        if 1 check each word
        if more than 3 - check if string exists within long string
    '''
    
    min_ = len(name)
    closest = ""
    
    for athlete in athletes_values_list:
        if iterative_levenshtein(athlete, name) < min_:
            min_ = iterative_levenshtein(athlete, name)
            closest = athlete
    return [name,closest,min_] if min_ > 0 else ''

unmatched_athletes = []
        
for athlete in athletes[:100]:
    if len(athlete) > 0:
        x = leven_score(athlete)
        if len(x) > 0: unmatched_athletes.append(x)

#%%

with pd.ExcelWriter(out_file) as writer:
    
    df = pd.DataFrame(unmatched_athletes)
    #df = df.transpose()
    df.columns = ["Athlete", "Closest", "Min"]
    df.to_excel(writer)
    
    workbook = writer.book
    format = workbook.add_format({'text_wrap': True})	
    
    writer.sheets['Sheet1'].set_column("B:B",75, format)	
    writer.sheets['Sheet1'].set_column("C:C",40, format)	
    
writer.save()
writer.close()    
#%%       


#for x in ['braulio', 'yuri simoes','edwin najmi','gabriel arges']:
 #   print('\'{}:[\'{}\'],'.format(x,x))