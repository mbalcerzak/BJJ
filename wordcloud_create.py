#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#import numpy as np
#from PIL import Image
#
## Create some sample text
#text = ' '.join([x for x in favourive_single if x not in own_sw])
#
#image_path = r"C:\Users\malgo_000\Pictures\BJJ wordcloud\belt_colours2.png"
#
#alice_coloring = np.array(Image.open(image_path))
#stopwords = set(STOPWORDS)
#stopwords.add("said")
#
#
#wc = WordCloud(background_color="white", max_words=600, mask=alice_coloring,
#               stopwords=stopwords, max_font_size=150, random_state=42)
#
#wc.generate(text)
#
#image_colors = ImageColorGenerator(alice_coloring)
#
#plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
#plt.axis("off")
#
#plt.show()
#
#wc.to_file(r'C:\Users\malgo_000\Pictures\wordcloud_bjj.png')