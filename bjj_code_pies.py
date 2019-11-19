#############  pie chart visualising the answers  #####################

def pie_chart_generator(question):
    question_list = data[question][data[question] != '']
    #data[question][data[question] == ''] = 'No answer'
    
    counts = Counter(question_list[2:].tolist())
    plt.pie([int(v) for v in counts.values()], labels=[str(k) for k in counts.keys()],
             autopct='%.1f%%')
    plt.show()

################## Q55 - gender ##################
#print(colnames_dict['Q55'])
pie_chart_generator('Q55')

################## Q56 - education - barchart ##################
#print(colnames_dict['Q56'])

def bar_plot(question):
    question_list = data[question][data[question] != '']
    #data[question][data[question] == ''] = 'No answer'
    
    counts = OrderedDict(Counter(question_list[2:]).most_common())
    
    plt.barh(range(len(counts)), list(counts.values()), align='center')
    plt.yticks(range(len(counts)), list(counts.keys()))
    
    plt.show()
    
bar_plot('Q56')

bar_plot('Q2')



pie_chart_generator('age_category')

################## Q57.1 - income ################
#print(colnames_dict['Q57.1'])
bar_plot('Q57.1')

################## Q59 - race / ethnicity #################
#print(colnames_dict['Q59'])
pie_chart_generator('Q59')

# what techniques are preffered by higher belts?
# belt promotion time Kaplan Meier
# do BJJ people buy naitonal brands?
# do higher belts compete more often?


data[['Q55','Q2']].groupby(['Q55','Q2']).size()

#############  pie chart visualising the answers  #####################

belt_colours = ['White belt','Blue Belt','Purple Belt','Brown Belt','Black Belt']

def pie_chart_by(question, gender = False, belt = False):
   
    if gender != False: 
        for gender_ in ('Female','Male'):
            question_list = data[question][(data[question] != '') & (data['Q55'] == gender_)]
            
            n = sum([1 for x in data['Q55'] if x == gender])
            
            counts = Counter(question_list[2:].tolist())
            plt.pie([int(v) for v in counts.values()], 
                     labels=[str(k) for k in counts.keys()],
                     autopct='%.1f%%')
            plt.title(gender_ + " (" + str(n) + ")")
            plt.show()
     
    if belt != False: 
        for belt_ in list(belt_colours.values()):
            question_list = data[question][(data[question] != '') & (data['Q2'] == belt_)]
            
            n = sum([1 for x in data['Q2'] if x == belt_])
            
            counts = Counter(question_list[2:].tolist())
            plt.pie([int(v) for v in counts.values()], 
                     labels=[str(k) for k in counts.keys()],
                     autopct='%.1f%%')
            plt.title(belt_ + " (" + str(n) + ")")
            plt.show()   
            
            
pie_chart_by('Q2', gender = True)

pie_chart_by('Q67.1', gender = True)   

pie_chart_by('Q67.1', belt = True)


cross = pd.crosstab(data['Q2'][data['Q2'].isin(belt_colours)], data['Q67.1'][data['Q67.1'] != ''])
cross_perc = cross.divide(cross.sum(axis=1), axis = 0)
cross_perc2 = pd.DataFrame(cross_perc, index = belt_colours)

cross2 = pd.DataFrame(cross, index = belt_colours)
techniques = ['Closed guard', 'Leg locking', 'Open Guard', 'Pressure Passing']
# Do preferences change over time?

# Make the plot
plt.stackplot(belt_colours, cross_perc['Closed guard'],cross_perc['Leg locking'],cross_perc['Open Guard'],cross_perc['Pressure Passing'], labels=techniques)
plt.legend(loc='upper left')
#plt.xticks(belt_colours)
plt.title('Favourite techniques vs. belt colour')
plt.show()

# Make the plot
plt.stackplot(belt_colours, cross_perc2['Closed guard'],cross_perc2['Leg locking'],cross_perc2['Open Guard'],cross_perc2['Pressure Passing'], labels=techniques)
plt.legend(loc='upper left')
#plt.xticks(belt_colours)
plt.title('Favourite techniques vs. belt colour')
plt.show()