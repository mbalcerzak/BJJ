from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 
from nltk.corpus import stopwords
sw = stopwords.words("english")
  
import pandas as pd
import os

from Functions.functions import clean_string

sw += ['aspect', 'new','something','thing','getting','every']

path = os.getcwd()

data = pd.read_csv(path + r'\BJJ1.csv')

favourite_raw = [x for x in data['Q19'][2:].to_list() if x == x]

check = '(@[A-Za-z]+)|([^A-Za-z \t\&])|(\w+:\/\/\S+)'

fav_clean = [clean_string(x,[],check).split() for x in favourite_raw]
fav_flat = [x for y in fav_clean for x in y if x not in sw]

text = ' '.join([lemmatizer.lemmatize(x) for x in fav_flat])

image_path = path + r"\belt_colours2.png"

alice_coloring = np.array(Image.open(image_path))
stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(background_color="white", max_words=700, mask=alice_coloring,
               stopwords=stopwords, max_font_size=160, random_state=42,
               collocations=False)

wc.generate(text)

image_colors = ImageColorGenerator(alice_coloring)

plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")

plt.show()

wc.to_file(path + r'\wordcloud_bjj.png')