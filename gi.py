import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
from nltk.corpus import stopwords
sw = stopwords.words("english")

#### My own python scripts from dictionary folder:

from Dictionaries.country_dictionary import country_dict

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


def clean_sub(string):
    string= string.lower()
    list_replacements = [['\'',''],[' & ','&']]
    
    for replacement in list_replacements:
        string = string.replace(replacement[0],replacement[1])

    check = '(@[A-Za-z0-9]+)|([^A-Za-z0-9 \t\&])|(\w+:\/\/\S+)'
    return ' '.join(re.sub(check, ' ', string).split())


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

