from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 
import nltk
nltk.download('stopwords') 

def create_wordcloud(fav_list, max_words, max_font_size, random_state):
        
    max_words = int(max_words.strip())
    max_font_size = int(max_font_size.strip())
    random_state = int(random_state.strip())
    
    from nltk.corpus import stopwords   
    
    sw = stopwords.words("english")
    sw += ['aspect', 'new','something','thing','getting','every', 'no answer']
  
    stopwords = set(STOPWORDS)   
      
    wc = WordCloud(background_color="white", max_words=max_words, 
                   stopwords=stopwords, max_font_size=max_font_size, 
                   random_state=random_state, collocations=False)
    
    wc.generate(fav_list)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    
    #plt.show()
    st.pyplot()