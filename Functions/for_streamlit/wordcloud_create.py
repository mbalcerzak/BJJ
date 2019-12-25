from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import streamlit as st
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 
import nltk
nltk.download('stopwords') 

def create_wordcloud(fav_list, max_words, max_font_size, random_state, image_path):
        
    max_words = int(max_words.strip())
    max_font_size = int(max_font_size.strip())
    random_state = int(random_state.strip())
    
    from nltk.corpus import stopwords   
    
    sw = stopwords.words("english")
    sw += ['aspect', 'new','something','thing','getting','every', 'no answer']
  
    coloring = np.array(Image.open(image_path))
    stopwords = set(STOPWORDS)   
    
    
    wc = WordCloud(background_color="white", max_words=max_words, 
                   mask=coloring, stopwords=stopwords, 
                   max_font_size=max_font_size, random_state=random_state,
                   collocations=False)
    
    wc.generate(fav_list)
    
    image_colors = ImageColorGenerator(coloring)
    
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    
    #plt.show()
    st.pyplot()