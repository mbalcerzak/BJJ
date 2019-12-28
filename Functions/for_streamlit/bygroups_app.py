# after choosing the 'SELECTED' option to see results for a specific group

import streamlit as st
import altair as alt

from Dictionaries.colnames_dictionary import header_dictionary as hd

##############################################################################
def bygroups_show(data, data_back_ma, data_current_ma, by_gr_dict, by_group):

    def norm_barchart(data_, q, column, count_, yn = False, order = False):
        
#        if yn == True:
#            color_ = alt.Color('{}:N'.format(column),
#                               scale=alt.Scale(domain=['No', 'Yes'], 
#                                               range=['darkorange', 'olivedrab']),
#                               legend=alt.Legend(title=''))
#        elif order == True:
#            color_ = alt.Color('{}:O'.format(column),
#                                scale=alt.Scale(scheme = 'yelloworangered'),
#                                legend=alt.Legend(title='')) #redyellowgreen 
#        else:
        color_ = alt.Color(column, 
                           scale = alt.Scale(scheme = 'darkmulti'),
                           legend=alt.Legend(title=''))
        
        data_ = data_[data_[column] != 'no answer']
    
        norm_bar = alt.Chart(data_).mark_bar().encode(
            y=alt.Y(by_gr_dict[by_group][0], title = '', 
                    sort = by_gr_dict[by_group][1]),
                    
            x=alt.X(count_, stack="normalize",
                    title = '',
                    axis=alt.Axis(format='%')),
            
            color = color_,
            tooltip = count_,
            order=alt.Order(column,sort = 'ascending')
            )
    
        st.subheader(hd[q])
        st.altair_chart(norm_bar)
        
    #-----------------------------------------------------------------------#
    
    
    #'Q2':'current_belt', 
        
    #'Q3':'training_years',
    norm_barchart(data, 'Q3','training_years','count(training_years)', order = True)  
    
    #'Q6':'white_blue',
    #'Q7':'blue_purple',
    #'Q8':'purple_brown',
    #'Q9':'brown_black',
    
    #'Q10':'training_per_week', 
    norm_barchart(data, 'Q10', 'training_per_week','count(training_per_week)', order = True) 
    
    #'Q11':'both_gi_nogi'
    norm_barchart(data, 'Q11', 'both_gi_nogi','count(both_gi_nogi)', yn = True)
    
    #'Q12':'gi_or_no_gi',
    norm_barchart(data, 'Q12', 'gi_or_no_gi','count(gi_or_no_gi)')
    
    #'Q13':'gym_self_defense',
    
    #'Q14':'training_time',
    norm_barchart(data, 'Q14', 'training_time','count(training_time)', order = True)  
    
    #'Q16':'travel',
    norm_barchart(data, 'Q16', 'travel','count(travel)',yn = True)  
    
    #'Q17':'background_ma',
    norm_barchart(data_back_ma, 'Q17', 'background_ma','count(background_ma)') 
    
    # Q18: Why did you start training jiu jitsu?
    # Q19: What is your favorite part about training?
    # Q20: What is your least favorite part about training?
    
    #'Q22':'how_old_when_started',
    norm_barchart(data, 'Q22', 'how_old_when_started', 'count(how_old_when_started)', order = True)  
    
    #'Q23':'instrutor_encourages_competition',
    
    #'Q24':'competed',
    norm_barchart(data, 'Q24', 'competed','count(competed)', yn = True) 
    
    #'Q25':'medals',
    #'Q26':'competition_organisation',
    #'Q27':'gym_curriculum',
    # Q28: Have you had any serious injuries from doing jiu jitsu
    
    #'Q30':'currently_cross_train',
    norm_barchart(data_current_ma, 'Q30', 'currently_cross_train', 'count(currently_cross_train)') 
    
    #'Q31':'mobility_exercises',
    norm_barchart(data, 'Q31','mobility_exercises','count(mobility_exercises)', yn = True) 
    
    #'Q32':'yoga',  
    norm_barchart(data, 'Q32', 'yoga','count(yoga)', yn = True) 
    
    #'Q33':'num_gis',
    norm_barchart(data, 'Q33', 'num_gis','count(num_gis)', order = True) 
    
    #'Q35':'num_rashguards',
    norm_barchart(data, 'Q35', 'num_rashguards','count(num_rashguards)', order = True) 
    
    #'Q38':'num_shorts',
    norm_barchart(data, 'Q38', 'num_shorts','count(num_shorts)', order = True) 
    
    # Q39: What are some of your favorite gi manufactures?
    # Q40: What are some of your favorite rash guard manufacturers?
    # Q41: What are some of your favorite short manufacturers?
    
    #'Q42':'bjj_apparel',
    norm_barchart(data, 'Q42', 'bjj_apparel','count(bjj_apparel)', yn = True) 
    
    # Q43: If you buy apparel, what are some of your favorite brands? If you 
    # don't buy apparel, leave blank!
    
    # Q44: Have you ever had a problem with a particular manufacturer or brand?
    # If so, which one(s) and what was the problem?
    
    #'Q47':'money_for_gear', # percent of income
    norm_barchart(data, 'Q47', 'money_for_gear','count(money_for_gear)', order = True) 
      
    #'Q48':'membership',
    
    #'Q49':'time_watching_bjj', 
    norm_barchart(data, 'Q49', 'time_watching_bjj','count(time_watching_bjj)', order = True) 
       
    # Q50: If you have some favorite grappling-related websites and blogs, 
    # which ones do you like?
    
    #'Q56':'education',
    #'Q55':'gender',
    #'Q57':'age',
    #'Q57.1':'income',
    #'Q59':'race',
    #'Q60':'do_watch_sport_bjj',
    
    #'Q60':'do_watch_sport_bjj',
    norm_barchart(data, 'Q60','do_watch_sport_bjj','count(do_watch_sport_bjj)', yn = True) 
    
    #'Q61.1':'where_watch_sport_bjj',
    
    #'Q62':'have_fav_athlete',
    norm_barchart(data, 'Q62', 'have_fav_athlete','count(have_fav_athlete)', yn = True) 
    
    # Q63: Who are your favorite athletes (if any)? As always, leave this 
    # blank if it doesn't apply to you!
    # Q65: If you have some favorite grappling-related podcasts, which ones 
    # do you like?
    # Q66: To which academy do you belong? If it is affiliated, what is the 
    # affiliation? For instance:  Oceanside BJJ - A Royce Gracie Affiliate
    #'Q66.1':'leg_lock_friendly',
    #'Q67':'nationality',
    
    #'Q67.1':'preferred_style'   
    norm_barchart(data, 'Q67.1', 'preferred_style','count(preferred_style)') 
    
    # Q68: What is your favorite submission?
    norm_barchart(data, 'Q69', 'choke','count(choke)')