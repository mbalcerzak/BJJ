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

athlete_dict = {
'AJ Azagarm':['aj azagarm'],
'Abraham Marte':['abraham marte'],
'Adam Benayoun':['adam benayoun'],
'Aleksander Karelin':['aleksander karelin'],
'Alexandre "Soca" Freitas':['alexandre "soca" freitas'],
'Alexandre Riberio':['alexandre riberio'],
'Aloisio Silva':['aloisio silva'],
'Alvaro Barreto':['alvaro barreto'],
'André Galvão':['andré galvão', 'andre galvao', 'galvao'],
'Angelica Galvao':['angelica galvao'],
'Antonio Braga Neto':['brags neto'],
'Antonio Rodrigo Nogueira':['antonio rodrigo nogueira'],
'Armando Wridt':['armando wridt'],
'Arthur Virgílio Neto':['arthur virgílio neto'],
'Augusto "Tanquinho" Mendes':['tanquinho mendes'],
'B.J. Penn':['b.j. penn', 'bj penn'],
'Bernardo Faria':['bernardo faria'],
'Bill Cooper':['bill cooper'],
'Brandon "Wolverine" Mullins':['brandon mullins', 'wolverine mullins'],
'Braulio Estima':['braulio estima', 'braulio'],
'Brian Ortega':['brian ortega'],
'Bruno Malfacine':['bruno malfacine', 'malfacine', 'malfisino'],
'Caio Terra':['caio terra'],
'Carley Gracie':['carley gracie'],
'Carlos "Bagana" Lima':['carlos "bagana" lima'],
'Carlos "Caique" Elias':['carlos "caique" elias'],
'Carlos Antonio Rosado':['carlos antonio rosado'],
'Carlos Gracie':['carlos gracie'],
'Carlos Gracie, Jr.':['carlos gracie, jr.'],
'Carlos Machado':['carlos machado'],
'Carlos Valente':['carlos valente'],
'Carlson Gracie':['carlson gracie'],
'Chael P. Sonnen':['chael p sonnen'],
'Charles Gracie':['charles gracie'],
'Chris Haueter':['chris haueter'],
'Christian Graugart':['christian graugart'],
'Clark Gracie':['clark gracie'],
'Claudinha Gadelha':['claudinha gadelha'],
'Cyborg  Abreu':['cyborg  abreu'],
'Danaher Death Squad':['danaher death squad', 'danaher group', 'dds'],
'Daniel "Raspberry Ape" Strauss':['raspberry ape'],
'Daniel Beleza':['daniel beleza'],
'Dave Camarillo':['dave camarillo'],
'Davi Ramos':['davi ramos'],
'Dean Lister':['dean lister', 'lister'],
'Demian Maia':['demian maia', 'damien maia', 'maia'],
'Derval Luciano Rêgo (Mestre Morcego)':['derval luciano rêgo (mestre morcego)'],
'Dillon Danis':['dillon danis'],
'Dominyka Obelenyte':['dominyka obelenyte'],
'Eddie Bravo':['eddie bravo', 'bravo'],
'Eddie Cummings':['eddie cummings', 'eddie cummins', 'cummings'],
'Eduardo Telles':['eduardo telles'],
'Edwin Najmi':['edwin najmi'],
'Emily Kwok':['emily kwok'],
'Enson Inoue':['enson inoue'],
'Erberth Santos':['erberth santos'],
'Eric Paulson':['eric paulson'],
'Fabio Gurgel':['fabio gurgel'],
'Fabricio Martins Costa':['fabricio martins costa'],
'Fabrício Werdum':['fabrício werdum', 'werdum'],
'Felicia Oh':['felicia oh'],
'Felipe Pena':['felipe pena'],
'Fernando "Terere" Augusto':['terere', 'fernando terere augusto'],
'Flavio Behring':['flavio behring'],
'Francisco Mansor':['francisco mansor'],
'Francisco Sá (Sazinho)':['francisco sá (sazinho)'],
'Fábio Santos (fighter)':['fábio santos (fighter)'],
'Gabriel Arges':['gabriel arges'],
'Gabrielle "Gabi" Garcia':['gabi garcia'],
'Garry Tonon':['garry tonon', 'tonon', 'gary tonon', 'garry tonnen'],
'Gastão Gracie':['gastão gracie'],
'Genki Sudo':['genki sudo'],
'Geny Rebello':['geny rebello'],
'Geo Martinez':['geo martinez'],
'Gezary Matuda':['gezary matuda', 'matuda', 'gezary'],
'Gianni Grippo':['gianni grippo', 'grippo'],
'Gilbert Burns':['gilbert burns'],
'Glover Teixeira':['glover teixeira', 'glover'],
'Gordon Ryan':['gordon ryan'],
'Gui Mendes':['gui mendes'],
'Guilherme Mendes':['guilherme mendes'],
'Gunnar Nelson':['gunnar nelson'],
'Hannette Staack':['hannette staack'],
'Helio Soneca':['helio soneca'],
'Helvecino Penna':['helvecio penna'],
'Hélio Gracie':['hélio gracie'],
'Igor Silva':['igor silva'],
'Isaac Doerderlein':['isaac doerderlein  sp'],
'JT Torres':['jt torres'],
'Jack Mcvicker':['jack mcvicker'],
'Jake Shields':['jake shields'],
'James Puopolo':['james puopolo'],
'Jean Jacques Machado':['jean jacques machado'],
'Jeff Glover':['jeff glover', 'glover'],
'Jeff Monson':['jeff monson'],
'Jeff Shaw':['jeff shaw'],
'Joao Miyao':['joao miyao'],
'Joaquim Valente':['joaquim valente'],
'Joe Moreira':['joe moreira'],
'Joe Rogan':['joe rogan'],
'John Danaher':['john danaher', 'danaher'],
'John Jones':['john jones'],
'Jon Satava':['jon satava'],
'Jorge (George) Gracie':['jorge (george) gracie'],
'Jorge Pereira':['jorge pereira'],
'Josh Barnett':['josh barnett', 'barnett'],
'Josh Hinger':['josh hinger'],
'João Alberto Barreto':['joão alberto barreto'],
'Kazushi Sakuraba':['kazushi sakuraba', 'sakuraba'],
'Keenan Cornelius':['keenan cornelious', 'keenan', 'cornelius'],
'Ken Gabrielson':['ken gabrielson'],
'Kennedy Maciel':['kennedy maciel'],
'Kenny Florian':['kenny florian'],
'Kit Dale':['kit dale'],
'Kobe Bryant':['kobe bryant'],
'Kron Gracie':['kron gracie', 'kron'],
'Kurt Osiander':['kurt osiander', 'ocieander', 'oisander', 'kurt ocieander'],
'Leandro Lo':['leandro lo'],
'Lebron James':['lebron james'],
'Leo Noguiera':['leo noguiera'],
'Leonardo "Leozinho" Vieira':['leozinho'],
'Leonardo Neves':['leonardo neves  coach'],
'Leticia Ribeiro':['leticia ribeiro'],
'Lucas Leite':['lucas leite'],
'Lucas Lepri':['lucas lepri'],
'Luis Carlos Guedes de Castro':['luis carlos guedes de castro'],
'Luis Franca':['luis franca'],
'Luiz França Filho':['luiz frança filho'],
'Luiz Fux':['luiz fux'],
'Luiz Palhares':['luiz palhares'],
'Léo Vieira':['léo vieira'],
'Mackenzie Dern':['mackenzie dern', 'mckenzie dern', 'meckenzie dern', 'makinzie dern', 'dern'],
'Marcelo Garcia':['marcelo garcia', 'marcello garcia', 'marcelo'],
'Marcelo Mattos':['marcelo mattos'],
'Marcio Andre':['marcio andre'],
'Marcio Cruz':['marcio cruz'],
'Marcos Tinoco':['marcos tinoco'],
'Marcus "Buchecha" Almeida':['marcus "buchecha" almeida', 'marcus buchecha almeida', 'marcus buchecha'],
'Marcus Almeida':['marcus almeida'],
'Marcus Buchecha':['buchecha'],
'Marcus Soares':['marcus soares'],
'Mark Hunt':['mark hunt'],
'Masakazu Iminari':['masakazu iminari'],
'Matheus Diniz':['matheus diniz'],
'Matt Serra':['early matt serra'],
'Mauricio Motta Gomes':['mauricio motta gomes'],
'Mendes Bros':['mendez', 'mendes', 'mendes bros', 'mendes brothers'],
'Michael Langhi':['michael langhi'],
'Michelle Nicollini':['michelle nicolini'],
'Mickey Gall':['mickey gall'],
'Milton Vieira':['milton vieira'],
'Miyao Brothers':['miao bros', 'miyao', 'miyao brothers', 'the miyaos'],
'Moises Muradi':['moises muradi'],
'Murilo Bustamante':['murilo bustamante'],
'Murilo Santana':['murilo santana'],
'Márcio Stambowsky':['márcio stambowsky'],
'Nate Diaz':['nate diaz'],
'Nathan Orchard':['nathan orchard'],
'Nelson Monteiro':['nelson monteiro'],
'Nicholas Meregali':['nicholas meregali'],
'Nick Diaz':['nick diaz'],
'Nino Schembri':['nino schembri'],
'Osvaldo Alves':['osvaldo alves'],
'Oswaldo Fadda':['oswaldo fadda'],
'Oswaldo Gracie':['oswaldo gracie'],
'Ottavia Bourdain':['ottavia bourdain'],
'Pablo Popovitch':['pablo popovitch'],
'Patrice Poissant':['patrice poissant'],
'Paulo Miyao':['paulo miyao'],
'Pedro Diaz':['pedro diaz'],
'Pedro Hemeterio':['pedro hemeterio'],
'Pedro Sauer':['pedro sauer'],
'Pedro Valente Sr.':['pedro valente sr.'],
'Rafael Barbosa Formiga':['formiga barbosa'],
'Rafael Lovato Jr.':['rafael lovato jr.', 'rafael lovato', 'lovato'],
'Rafael Mendes':['rafael mendes', 'rafa mendes', 'rafa'],
'Relson Gracie':['relson gracie'],
'Renato Paquet':['renato paquet'],
'Rener Gracie':['rener gracie'],
'Renzo Gracie':['renzo gracie'],
'Reyson Gracie':['reyson gracie'],
'Rhadi Ferguson':['rhadi ferguson'],
'Riberio Brothers':['riberio brothers', 'ribeiro bros'],
'Ricardo De La Riva':['ricardo de la riva'],
'Ricardo Murgel':['ricardo murgel'],
'Ricardo Vieira':['ricardo vieira'],
'Richie Martinez':['richie martinez'],
'Rickson Gracie':['rickson gracie', 'ricks on gracie', 'rickson'],
'Rigan Machado':['rigan machado'],
'Rilion Gracie':['rilion gracie'],
'Robert Drysdale':['robert drysdale'],
'Roberto "Cyborg" Abreu':['roberto "cyborg" abreu', 'cyborg', 'robert cyborg abreu'],
'Roberto Satoshi':['roberto satoshi'],
'Robson Gracie (Carlos Robson Gracie)':['robson gracie (carlos robson gracie)'],
'Robson Moura':['robson moura'],
'Rodoflo Viera':['rodoflo viera'],
'Rodolfo Vieira':['rodolfo vieira', 'rodolpho', 'rodolfo'],
'Rodrigo Comprido Medeiros':['comprido'],
'Roger Gracie':['roger gracie', 'roger'],
'Rolando Samson':['rolando samson'],
'Rolker Gracie':['rolker gracie'],
'Rolls Gracie':['rolls gracie'],
'Romero "Jacare" Cavalcanti':['romero "jacare" cavalcanti', 'jacare'],
'Romulo Barral':['romulo barral'],
'Ronaldo "Jacare" Souza':['ronaldo souza', 'jacare souza', 'ronaldo jacare'],
'Ronda Rousey':['ronda rousey'],
'Rorion Gracie':['rorion gracie'],
'Rousimar Palhares':['rousimar palhares'],
'Roy Dean':['roy dean'],
'Royce Gracie':['royce gracie', 'royce'],
'Royler Gracie':['royler gracie', 'royler'],
'Rubens "Cobrinha" Charles':['rubens "cobrinha" charles', 'cobrinha', 'rubens charles'],
'Ryan Hall':['ryan hall'],
'Ryron Gracie':['ryron gracie'],
'Saulo Ribeiro':['saulo ribeiro', 'saulo ribero', 'saulo'],
'Sergio "Malibu" Jardim':['sergio "malibu" jardim'],
'Shamil Gamzatov':['shamil gamzatov'],
'Shinya Aoki':['aoki', 'shinya', 'shinya aoki'],
'Stephan Kesting':['stephan kesting'],
'Sylvio Behring':['sylvio behring'],
'Sérgio Penha':['sérgio penha'],
'Tom Barlow':['tom barlow'],
'Travis Stevens':['travis stevens'],
'Valerie Worthington':['valerie worthington'],
'Vanderson Gomez':['vanderson gomez'],
'Vinny Magalhães':['vinny magalhães'],
'Vitor Ribeiro':['vitor ribeiro'],
'Wellington "Megaton" Dias':['wellington "megaton" dias', 'megaton'],
'Wilson Mattos':['wilson mattos'],
'Xande Ribeiro':['xande ribeiro', 'xande', 'xande ribiero'],
'Yuri Simoes':['yuri simoes', 'i ve recently become a fan of yuri simoes'],
'Yvonne Duarte':['yvonne duarte']
 }

#%%
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
    
    string =  re.sub(check, ' ', string).strip()
    
    return ' '.join([x for x in string.split(' ') if x not in sw])

athletes = []
for row in althetes_list:
    clean_row = row.replace('.',',').replace('/',',').replace(' and ',',')
    athletes += [clean_sub3(x) for x in clean_row.split(',') if x != '']

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

for key, value in sorted(athlete_dict.items()):
    print("\'{}\':{},".format(key,value))

#%%

lista_do_dict = []

dict_ = {}

for elem in lista_do_dict:
    print("\'{}\':[\'{}\'],".format(elem.title(),elem))
