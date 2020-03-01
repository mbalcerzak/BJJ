import streamlit as st
import altair as alt
import plotly.express as px
from collections import Counter

from Dictionaries.colnames_dictionary import header_dictionary as hd
from Dictionaries.colnames_dictionary import colnames_dictionary as col_d

def overall_show(data, data_current_ma, data_back_ma, data_reasons, 
                 data_least_f, data_subs, data_podcast, data_web, data_gi, 
                 data_rash, data_shorts, data_apparel, data_comp, data_injury, 
                 data_athlete, data_watch, colour, by_gender = False, 
                 by_belt = False, selected = False):
 
    def bar_plot(data, q, column, colour = colour):    
          
        counts = data[column].value_counts()[:15].index.tolist()          
        data = data[data[column].isin(counts)]        
        
        data_bars = len(data[column].unique())   
        
        bars = alt.Chart(data, height = data_bars * 20).mark_bar( \
                            color = colour).encode( #, opacity = 0.8
                            x = alt.X('count(current_belt)', 
                                      title = 'Number of times mentioned'),
                            y = alt.Y(column, 
                                      sort = alt.EncodingSortField(
                                                  field='current_belt', 
                                                  op="count", 
                                                  order='descending'),
                                      title = '' ),
                            tooltip = 'count(current_belt)'). \
                            configure_axis(labelFontSize=15,
                                           titleFontSize=15)
        
        st.subheader(hd[q])
        bars.width = 500
        st.altair_chart(bars)
    
    def pie_chart(data, q, title_ = None):
        
        if 'Q' in q:
            question = col_d[q]
        else:
            question = q
        
        data = data[data[question] != 'no answer']
            
        counts = Counter(data[question].to_list())
        
        category = [str(k) for k in counts.keys()]
        count = [int(v) for v in counts.values()]
        
        fig = px.pie(data, values = count, names = category,
                     color_discrete_sequence=px.colors.sequential.YlGnBu[::-1])
        
        fig.update_layout(autosize = False, width = 600, height = 400)
    
        if title_ == None:
            title_ = hd[q]
    
        st.subheader(title_)
        st.plotly_chart(fig) 
    
    
    # Q2: What is your current rank in jiu jitsu?
    if by_belt == False: 
        pie_chart(data,'Q2')
    
    # Q3: How long have you been training jiu jitsu?
    pie_chart(data,'Q3')
 
    if by_belt == False: 
        # Q6: How long did it take you to go from white belt to blue belt?
        pie_chart(data,'Q6')
        
        # Q7: How long did it take you to go from blue belt to purple belt?
        pie_chart(data,'Q7')
        
        # Q8: How long did it take you to go from purple belt to brown belt?
        pie_chart(data,'Q8')
        
        # Q9: How long did it take you to go from brown belt to black belt?
        pie_chart(data,'Q9')
    
    # Q10: On average, how many times do you train per week?
    pie_chart(data,'Q10')
    
    # Q11: Do you train both gi and no-gi?
    pie_chart(data,'Q11') 
    
    # Q12: Do you prefer training gi or no-gi?
    pie_chart(data,'Q12')
    
    if selected == False: 
        # Q13: Does your academy focus on self-defense?
        pie_chart(data,'Q13')
     
    # Q14: What is your preferred time to train?
    pie_chart(data,'Q14') 
    
    # Q16: Do you train at gyms when you travel?
    pie_chart(data,'Q16') 
    
    # Q17: Did you have a background in another martial art before you started
    # jiu jitsu?  If so, which one(s)?
    pie_chart(data_back_ma,'Q17') 
    
    # Q18: Why did you start training jiu jitsu?
    bar_plot(data_reasons, 'Q18', 'reasons')  
    
    # Q19: What is your favorite part about training?
    # wordcloud
    
    # Q20: What is your least favorite part about training?
    bar_plot(data_least_f, 'Q20', 'least_favourite') 
    
    # Q22: How old were you when you started jiu jitsu?
    pie_chart(data,'Q22') 
    
    if selected == False: 
        # Q23: Does your instructor encourage students at your gym to compete?
        pie_chart(data,'Q23') 
    
    # Q24: Have you competed in jiu jitsu before?
    pie_chart(data,'Q24') 
    
    # Q25: If you have competed, have you won any of the following medals?
    #pie_chart(data,'Q25')
     
    # Q26: If you have competed, what was the organization (e.g., IBJJF, NAGA, 
    # etc.)? Fill in as many as apply!
    bar_plot(data_comp, 'Q26', 'organisations')  
    
    if selected == False: 
        # Q27: Does your gym have a formal curriculum?
        pie_chart(data,'Q27')
     
    # Q28: Have you had any serious injuries from doing jiu jitsu (that is, 
    # injuries that required weeks or months off or perhaps even surgery?) 
    # If so, please list the injuries and very briefly explain how they 
    # occurred and how long it took to recover--e.g., ACL tear via heel hook 
    # with 9 month recovery.
    bar_plot(data_injury, 'Q28', 'injuries') 
    
    # Q30: Do you cross-train in other martial arts? If so, which one(s)?
    pie_chart(data_current_ma,'Q30') 
    
    # Q31: Do you do mobility exercises to prepare your body for jiu jitsu 
    #(e.g., ginastica natural)?
    pie_chart(data,'Q31') 
    
    # Q32: Do you do yoga to prepare your body for jiu jitsu?
    pie_chart(data,'Q32') 
    
    # Q33: How many gis do you own?
    pie_chart(data,'Q33') 
    
    # Q35: How many rash guards do you own?
    pie_chart(data,'Q35') 
    
    # Q38: How many no-gi shorts do you own?
    pie_chart(data,'Q38') 
    
    # Q39: What are some of your favorite gi manufactures?
    bar_plot(data_gi, 'Q39', 'gi') 
    
    # Q40: What are some of your favorite rash guard manufacturers?
    bar_plot(data_rash, 'Q40', 'rash') 
    
    # Q41: What are some of your favorite short manufacturers?
    bar_plot(data_shorts, 'Q41', 'shorts') 
    
    # Q42: Do you buy jiu jitsu apparel (e.g., tee shirts, hats, etc.)?
    pie_chart(data,'Q42')
     
    # Q43: If you buy apparel, what are some of your favorite brands? If you 
    #don't buy apparel, leave blank!
    bar_plot(data_apparel, 'Q43', 'apparel') 
     
    # Q47: How much do you spend per year (on average) on gear and apparel?
    pie_chart(data,'Q47') 
    
    if selected == False: 
        # Q48: How much do you spend per month for membership dues?
        pie_chart(data,'Q48')
     
    # Q49: How much time do you spend per day (on average) reading or watching 
    #jiu jitsu-related material?
    pie_chart(data,'Q49')
     
    # Q50: If you have some favorite grappling-related websites and blogs, 
    # which ones do you like?
    bar_plot(data_web, 'Q50', 'website') 
    
    if by_gender == False: 
    # Q55: What is your gender?
        pie_chart(data,'Q55')
     
    # Q56: What is your education level? Please select the highest degree 
    # you've completed.
    pie_chart(data,'Q56') 
    
    # Q57: What is your age?
    #pie_chart(data,'Q57') 
    pie_chart(data,'age_cat','How old are you?')
     
    # Q57.1: What is your income?
    pie_chart(data,'Q57.1') 
     
    # Q59: What is your race/ethnicity?
    pie_chart(data,'Q59') 
     
    # Q60: Do you watch sport jiu jitsu?
    pie_chart(data,'Q60') 
    
    # Q61.1: If you do watch sport jiu jitsu, what do you watch and where do 
    # you watch it? For instance, do you watch PPVs?  If so, which 
    # organizations--EBI, Metamoris, Polaris, etc.
    bar_plot(data_watch, 'Q61.1', 'watch_sport')
    
    # Q62: Do you have a favorite jiu jitsu athlete or athletes?
    pie_chart(data,'Q62') 
     
    # Q63: Who are your favorite athletes (if any)? As always, leave this 
    # blank if it doesn't apply to you!
    bar_plot(data_athlete, 'Q63', 'athletes')
    
    # Q65: If you have some favorite grappling-related podcasts, which ones 
    # do you like?
    bar_plot(data_podcast, 'Q65', 'podcast')
    
    # Q66: To which academy do you belong? If it is affiliated, what is the 
    # affiliation?REAMLIT 
    #pie_chart(data,'Q66') 
    
    if selected == False:
        # Q66.1: Is your gym "leg lock friendly"?
        pie_chart(data,'Q66.1')  
    
    # Q67: Where is your nationality?
    bar_plot(data, 'Q67', 'country') 
    
    # Q67.1: What is your preferred "style"?
    pie_chart(data,'Q67.1')  
    
    # Q68: What is your favorite submission?
    bar_plot(data_subs, 'Q68', 'technique') 
    
    # Q69: Is your favourite sumbission a choke?
    pie_chart(data,'Q69')  