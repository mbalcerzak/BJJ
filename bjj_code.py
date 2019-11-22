import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
from nltk.corpus import stopwords
sw = stopwords.words("english")


#path = 'C:/Users/malgo_000/Desktop/BJJ/'
path = r"C:\Users\kkql180\OneDrive - AZCollaboration\BJJ\BJJ_dataset"


# getting the data and deleting unimportant columns
data = pd.read_csv(path + '\BJJ1.csv')
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

################## 1. Country Q67 --> "nationality"  #################

def generate_country_dict():
    country_dict = {
            'USA':['US','USA','States','American','america','Murrica','Murika',
                   'Murica','Virginia','Texan','Merica','Merican','Merkin'],
            'UK':['English','England','Scottish','Britain','British','Kingdom',
                  'Welsh','Scotland','UK'],
            'Netherlands':['NL','Dutch','Netherlands','Netherland',],
            'Ireland':['Irish','Ireland'],
            'Italy':['Italian','Italy'],
            'Germany':['German','Deutsch','getman','DE','Germany'],
            'Australia':['Australian', 'Austtalian','Australia'],
            'India':['Indian','India'],
            'Canada':['Canadian','Canada'],
            'Phillipines':['Filipino','Phillipines','Philippines'],
            'France':['French','France'],
            'Poland':['Polish','Poland'],
            'Japan':['Japanese','Okinawan','Japan'],
            'Brazil':['Brazilian','Brazillian', 'Brazil'],
            'Israel':['Israeli','Israel'],
            'Portugal':['Portuguese','Portugal'],
            'Iceland':['Icelandic','Iceland'],
            'Lithuania':['Lithuanian','Lithuania'],
            'Singapore':['Singaporean','Singapore'],
            'New Zealand':['NewZealander','NewZealand'],
            'Norway':['Norwegian','Norway'],
            'Colombia':['Colombian','Colombia'],
            'Vietnam':['Vietnamese','Vietnam'],
            'Denmark':['Danish','DK','Denmark'],
            'Sweden':['Swedish','Sweden'],
            'Uruguay':['Uruguayan','Uruguay'],
            'Pakistan':['Pakistani','Pakistan'],
            'Austria':['Austria','Austrian'],
            'Nicaragua':['Nicaragua'],
            'Russia':['Russian','Russia'],
            'China':['Chinese','China'],
            'Switzerland':['Swiss','Switzerland'],
            'Hungary':['Hungary','Hungarian'],
            'Serbia':['Serbian','serb','Serbia'],
            'Romania':['Romanian','Romania'],
            'Finland':['Finnish','Finland'],
            'Croatia':['Croatian','Croatia','cro'],
            'Bosnia':['Bosniak','Bosnian','Bosnia'],
            'South Africa':['SouthAfrican','SouthAfrica','SouthAfrican'],
            'Mexico':['Mexican','Mexico'],
            'Malaysia':['Malaysian','Malaysia'],
            'Greece':['Greek','Greece'],
            'South Korea':['Korean','Korea','SouthKorea'],
            'Egypt':['Egyptian','Egypt'],
            'Ecuador':['Ecuadorian','Ecuador'],
            'Spain':['Spanish','Spain'],
            'Czech Republic':['Czech'],
            'Ukraine':['Ukranian','Ukraine'],
            'Chile':['Chile'],
            'Turkey':['Turkish','Turkey'],
            'Indonesia':['Indonesia'],
            'Jamaica':['Jamaica'],
            'Cuba':['Cuban','Cuba'],
            'Macedonia':['Macedonian','Macedonia'],
            'Malta':['Maltese','Malta'],
            'Montenegro':['Montenegrin'],
            'Other':['Other'],
            'watch bjj':['watch bjj','watchbjj']
            }
    
    country_dict2 = {}  
    for c_list, country in zip(list(country_dict.values()), country_dict.keys()):
        for c in c_list:
            country_dict2[c.lower()] = country
    
    return country_dict2

country_dict = generate_country_dict()


def clean_text(string):
    string= string.lower()
    list_replacements = [['.',''],['new ','new'],['south ','south']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z]+)|([^A-Za-z \t\&])|(\w+:\/\/\S+)'
    return (' '.join(re.sub(check, ' ', string).split())).split(' ')

data_q['country_list'] = [clean_text(x) for x in data_q['Q67']]

def country_get(word_list):
    nationalities = []
    
    for word in word_list:
        nationality = ''
        if word.lower() in country_dict.keys():
            nationality = country_dict[word.lower()]
        if nationality != '' and nationality not in nationalities:
            nationalities.append(nationality)      
        if nationality == 'Other':
            break
    
    return nationalities
        
data_q['nationality'] = [country_get(x) for x in data_q['country_list']] 
  
################## Q57 - age ##################

def age_categories(x):   
    if x == x and x != '':
        return '{}-{}'.format(round(int(x)//5*5),round(int(x)//5*5+5))
    
data_q['age_category'] = data_q['Q57'].apply(age_categories)  

##### Overall, do not split into belts or gender:
data_all = data_q[["Q57", "Q55", "age_category", "nationality", "Q59", "Q56", "Q57.1", "Q22"]]

############### [18,19,20,28],  Wordcloud ##############

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
    
##################   Gi i NoGi ulubione ciuchy  #########################

data_gi = data_q[["Q39","Q40","Q41","Q43"]]

def create_gi_company_list(dataset, columns):
    gi_list = []
    
    for col in columns:
        column = dataset[col][dataset[col] != ''].tolist()
        
        for row in column:
            gi_list += row.split(',')
    
    return [clean_sub(x) for x in gi_list if clean_sub(x) not in sw]
        
gi_list = create_gi_company_list(data_q, ["Q39","Q40","Q41","Q43"])

'''
def most_frequent(List): 
    occurence_count = Counter(List)
    #print(occurence_count.most_common())
    return [x[0] for x in occurence_count.most_common()]
'''
   
#print(most_frequent(gi_list))     
    
    
gi_dict = {
        'tatami':['tatami','tatame','tatiama','roots','tank'],
        'scramble':['scramble','scrable'], 
        'toro':['toro','torro','tora','tori'], 
        'fuji':['fuji','fugi','fujji','mission 22','victory'], 
        '93 brand':['93'], 
        'shoyoroll':['shoyoroll','shoyaroll','shoyroll','shoyo','syr','97'],
        'atama':['atama','atami'],
        'venum':['venum','venom','venu'],
        'manto':['manto','manti'], 
        'hayabusa':['hayabusa','haybusa','hyubasa','hayabusha'],
        'newaza':['newaza'],
        'gameness':['gameness','air'],
        'kingz':['kingz','kings'],
        'hyperfly':['hyperfly','hyper fly','hyperlyte','doordie'],
        'adidas':['adidas'],
        'underarmour':['underarmor','underarmour','under armor',' ua '],
        'globetrotters':['globetrotters'],
        'hypnotic':['hypnotic','hypnotik'],
        'valor':['valor','valot'],
        'meerkatsu':['meerkatsu'],
        'cageside':['cageside'],
        'fightwear':['fightwear'],
        'vulkan':['vulkan','vulcan'],
        'ctrl':['ctrl','ctr ','cntrl'],
        'storm':['storm'],
        'nike':['nike'],
        'jaco':['jaco'],
        'quicksilver':['quicksilver'],
        'lanky fightgear':['lanky'],
        'break point':['breakpoint'],
        'datsusara':['datsusara'],
        'inverted gear':['inverted'],
        'koral':['koral'],
        'cageside ':['cageside'],
        'keiko':['keiko','keiki'],
        'rvca':['rvca'],
        'phalanx':['phalanx'],
        'tapout':['tapout'],
        'fushida':['fushida'],
        'rip stop':['rip stop','ripstop'],
        'billabong':['billabong'],
        'sprawl':['sprawl','spawl'],
        'on the mat':['otm'],
        'keiko raca':[ 'keiko raca','kenka'],
        'padilla and sons':['padilla and sons','padillo and sons','padilla&sons'],
        'double weave judo gi':['double weave', 'judo gi'],
        'wallmart':[ 'walmart','wallmart','wal mart'],
        'gi pants':['gi pants'],
        'academy / tournaments':['school','gym','club','seminars','tournaments','competition','in house'],
        'message':['comedic','message','goku','puns','stuff that says'],
        'travel & shopping':['travel'],
        'gracie':['gracie'],
        'sanabul':['sanabu'],
        'war tribe':['war tribe'],
        'deus':['deus'],
        '10th planet':['10th planet'],
        'raven':['raven'],
        'flow':['flow'],
        'dragao':['dragao'],
        'fluid surf':['fluid surf'],
        'do or die':['do or die'],
        'killer bee':['killer bee'],
        'da firma':['da firma','dafirma','dkfc'],
        'xguard':['xguard','x guard'],
        'xarmor':['xarmor'],
        'lycan':['lycan'],
        'champion':['champion'],
        'budo':['budo'],
        'american top team':['att'],
        'jiujiteiro':['jiujiteiro','jiujitero','jiujitiero','jiu jiteiro'],
        'braus fight':['braus','braus fight'],
        'igear':['igear'],
        'grab & pull':['grab pull','grab&pull'],
        'grips':['grips'],
        'isami':['isami'],
        'devine':['devine'],
        'strike fightwear':['strike fight wear','strike','strikefightwear'],
        'combat corner':['combatcorner'],
        'fairtex':['fairtex'],
        'origin':['origin'],
        'bad boy':['bad boy','badboy','babboy'],
        'progress':['progress'],
        'sub apparel':['sub apparel'],
        'lucky gi':['lucky','lucki'],
        'scartissue':['scartissue'],
        'phantom':['phantom'],
        'reversal':['reversal'],
        'oss clothing':['oss'],
        'high type':['hightype'],
        'throwdown':['throwdown'],
        'tokyo five':['tokyo five','tokyo 5'],
        'choke aloha':['choke aloha','chokealoha','choke'],
        'ecko':['ecko'],
        'furia':['furia'],
        'redstar':['redstar'],
        'roots of fight':['roots of fight'],
        'torque':['torque'],
        'takedown nation':['takedown nation'],
        'open guard apparel':['open guard apparel'],
        'blank kimonos':['blank'],
        'brazilian fightwaer':['brazilian fightware','brazilian '],
        'vhts':['vhts'],
        'triangle athletics':['triangle athletics'],
        'sub sport':['sub sport','amazon','sub sports'],
        'rios gear':['rios'],
        'ouano':['ouano','ouani'],
        'nogi industries':['nogi industries','nogi brand'],
        'bc kimonos':['bc kimonos'],
        'illest':['illest'],
        'vambora fight gear':['vambora fight gear','vamborabjj'],
        'warrior kimonos':['warrior'],
        'grapplers quest':['grapplers quest'],
        'bamboo':['bamboo break'],
        'gorilla fight gear':['gorilla fight gear'],
        'gawakoto':['gawakoto'],
        'last resort fightwear':['last resort fightwear'],
        'eastbay':['eastbay'],
        'arm bar soap':['soap'],
        'fokai':['fokai'],
        'affliction':['affliction'],
        'dokebi combat outfitters':['dokebi bros'],
        'fabulous gi':['fabulous gi'],
        'ck fight life':['contract killer'],
        'doguera':['dogueira'],
        'forty thieves':['forty thieves'],
        'ground fighter':['ground fighter'],
        'kipsta':['kipsta'],
        'kauai':['kauai'],
        'krugans':['krugans'],
        'kraken':['kraken'],
        'koa mill':['koa mill'],
        'infiniti':['infiniti'],
        'inspirit':['inspirit'],
        'fusion':['fusion'],
        'jotunn':['jotunn'],
        'bull terrier':['bull terrier','peel'],
        'buffalo combat':['buffalo'],
        'your jiu jitsu gear':['yourbjjgear'],
        'virus':['virus'],
        'brazil combat':['brazil combat'],
        'dethrone royalty brand':['dethrone'],
        'prana':['prana'],
        'reevo':['reevo'],
        'tribos':['tribos'],
        'toraki':['toraki'],
        'punch town':['punch town'],
        'shiroi':['shiroi'],
        'submission sniper':['submission sniper'],
        'triumph united':['triumph united'],
        'tuff fightwear':['tuff'],
        'studio 540':['studio 540'],
        'megami':['megami'],
        'mizuno':['mizuno'],
        'jiu jitsu progear':['jiu jitsu progear'],
        'holdfast':['holdfast'],
        'revgear':['rev gear'],
        'tatsumi':['tatsumi'],
        'ok! kimonos':['ok kimonos'],
        'lonsdale':['lonsdale'],
        'moka hardware':['moka'],
        'predator':['predotor gi'],
        'alma':['alma'],
        'bj penn':['bj penn'],
        'sirius':['sirius'],
        'senor kimonos':['senor kimonos'],
        'old man jiu jitsu':['omjj'],
        'isso apparel':['isso apparel'],
        'nor cal fight shop':['norcal fight shop'],
        'ronin brank kimonos':['ronin'],
        'springroll fightwear':['springroll'],
        'platinum jiujitsu':['platinum'],
        'hylete':['hylete'],
        'sinister':['sinister'],
        'nine lives':['9 lives'],
        '31fifty':['31fifty'],
        'mvnt brand':['mvnt'],
        'muae':['muae'],
        'moy':['moy'],
        'macaco branco':['macaco branco'],
        'nous defions':['nous defions'],
        'pony club grappling gear':['pony club grappling gear'],
        'rcj machado gear':['rcj machado apparel'],
        'just saiyan gear':['just saiyan'],
        'yolo bjj':['yolo'],
        'howard combat kimonos':['hck'],
        'want vs need':['want vs need']
        }    


###################  Academies ######################################

data_acedmy = data_q[["Q13","Q66","Q27","Q66.1"]]

def create_academy_list(dataset, columns):
    gi_list = []
    
    for col in columns:
        column = dataset[col][dataset[col] != ''].tolist()
        
        for row in column:
            gi_list += row.split(',')
    
    return [clean_sub(x) for x in gi_list if clean_sub(x) not in sw]
        

academy_list = create_academy_list(data_q, ["Q66"])


academy_dict = {
        
        '10th planet':['10th planet'],
        'alliance':['alliance'],
        'capital mma':['capital mma','capitol takoma','capital mm'],
        'chapel hill':['chapel hill'],
        'carlson gracie':['carlson gracie'],
        'devine':['devine'],
        'gracie barra':['gracie barra'],
        'next generation':['next generation'],
        'renzo gracie':['renzo gracie'],
        'royce gracie':['royce gracie','royce affiliate'],
        'roger gracie':['roger gracie'],
        'roger machado':['roger machado'],
        'checkmat':['checkmat'],
        
        
        }




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

#%%
media_dict = {
         '10th planet':['10th planet','10thplanet'],
         'reddit':['r/','reddit'],
         'budo':['budo'],
         'stephan kesting': ['stephan kesting'],
         'roy dean': ['roy dean'],
         'adcc': ['adcc'],
         'youtube': ['youtube','you tube'],
         'adam benayoun': ['adam benayoun'],
         '40plusbjjsuccess': ['40plusbjjsuccess'],
         'ebi': ['ebi'],
         'bjj scout': ['bjj scout', 'bjjscout'],
         'bj penn': ['bj penn'],
         'bjj eastern europe': ['bjj eastern europe','bjj ee', 'bjj easter europe',
                                'bjj eastern eirope','bjjee','eastern eu','eebjj',
                                'bjjeastern', 'bjjeasteneurope'],
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
         'kurt osiander': ['kurt osiander','ocieander','oisander','kurt o'],
         'joe rogan': ['rogan'],
         'saulo': ['saulo','saul'],
         'sherdog': ['sherdog'],
         'rickson': ['rickson','ricks on'],
         'ryan hall': ['ryan hall'],
         'savagekitsune': ['savagekitsune'],
         'sharkgirlbjj': ['sharkgirlbjj'],
         'tristargym': ['tristargym'],
         'tom barlow': ['tom barlow'],
         'rafael lovato': ['rafael lovato'],
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
         'john danaher': ['john danaher'],
         'mendes bros':['mendez','mendes'],
         'marcelo garcia': ['marcelo garcia','marcello garcia'],
         'aj azagarm': ['aj azagarm'],
         'andre galvao': ['andre galvao'],
         'eddie bravo': ['eddie bravo'],
         'marcus buchecha': ['buchecha'],
         'kron gracie': ['kron gracie'],
         'keenan cornelious': ['keenan cornelious','kennnan kornelius', 
                               'keenan cornelius','keenan cornielius',
                               'keenan kornelius','kennen cornelius','keenan'],
         'roger gracie':['roger gracie'],
         'miyao brothers':['miao bros','miyao'],
         'renzo gracie': ['renzo gracie'],
         'bjj brick': ['bjj brick','bjjbrick'],
         'mixedmartialarts': ['mixedmartialarts'],
         'mackenzie dern': ['mackenzie dern','mckenzie dern','meckenzie dern'],
         'fight to win':['fight to win','fight 2 win','fight2win'],
         'meerkatsu blog': ['meerkatsu blog'],
         'eddie cummings': ['eddie cummings','eddie cummins'],
         'flo grapplimg': ['flo grapplimg','flograpplimg'],
         'flow grappling': ['flow grappling','flowgrappling', 'flo'],
         'mma junkie': ['mma junkie'],
         'bloody elbow': ['bloody elbow'],
         'ppv':['ppv'],
         'live':['live'],
        'fightpass':['fightpass'],
        'white belt bjj':['white belt'],
        'royce gracie':['royce'],
        'rickson gracie':['rickson gracie', 'ricks on gracie', 'rickson'],
        'michael langhi':['michael langhi'],
        'rodolfo vieira':['rodolfo vieira','rodolpho viera','rodalfo vierrea', 'rodoflo viera','rodolfo', 'rodolfo vieira', 'rodolfo viera'],
        'cobrinha':['cobrinha'],
        'maxbjj':['maxbjj'],
        'bjj library':['bjjlibrary', 'bjj library'],
        'jiu jitsu style': ['jiu jitsu style'],
         'grapplers guide': ['grapplers guide','grapplersguide'],
         'instagram': ['instagram'],
         'inverted gear': ['inverted gear'],
         'insidebjj': ['insidebjj'],
         'damian maia':['damian maia'],
         'otm':['otm'],
         'friends compete':['teammate','friend'],
         'grappling central':['grappling central', 'grapplingcentral']
        }


list_do_dict = [
        'bjj over 40', 
        ]


for elem in list_do_dict:
    media_dict[elem] = [elem]

media_dict

#%%



def most_frequent(List): 
    occurence_count = Counter(List)
    #print(occurence_count.most_common())
    return [x[0] for x in occurence_count.most_common()]

unsorted = most_frequent(media_list)
#print(sorted(unsorted))

    