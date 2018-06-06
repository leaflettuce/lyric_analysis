# -*- coding: utf-8 -*-
"""
Create word bubble from lyric csv
"""
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pylab as plt
from wordcloud import WordCloud, STOPWORDS


# import
me = pd.read_csv("data/mount_eerie.csv")

# aggregate all lyrics togther
lyrics = ""
for i in me['lyrics']:
    lyrics = lyrics + i
 
#clean up
lyrics = lyrics.replace('\\n', ' ').replace("\"",'').replace('\'', '').replace('-','').replace(',', '')
lyrics = lyrics.replace('[', '').replace(']', '').replace('(','').replace(')', '').replace('/','').replace('.','')
lyrics = lyrics.lower()

#split by words
words = [t for t in lyrics.split()] 


#remove stop words
cleaned_words = words
for word in words:
    if word in stopwords.words('english'):
        cleaned_words.remove(word)
        
# unique words and plot
freq = nltk.FreqDist(cleaned_words) 

#manually remove some
word_dict = {}
for i in freq:
    word_dict[i.lower()] = freq[i]
    
del word_dict['the']
del word_dict['and']
del word_dict['i']
del word_dict['a']
del word_dict['in']
del word_dict['my']
del word_dict['your']
del word_dict['to']
del word_dict['but']
del word_dict['go']
del word_dict['i\m']
del word_dict['im']
del word_dict['with']
del word_dict['to']
del word_dict['so']
del word_dict['this']
del word_dict['is']
del word_dict['you']
del word_dict['me']
del word_dict['see']
del word_dict['do']


# plot
words_listed = sorted(word_dict.items())
x, y = zip(*words_listed)
plt.plot(x, y)
plt.show()


#lemmatize
lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize('died')) 

#bubbler
wc = WordCloud(height = 500, width = 1000, background_color="darkgrey", max_words=2000,
               stopwords=stopwords, max_font_size=100, random_state=42, relative_scaling = .5,
               colormap = 'ocean')

wc = wc.generate_from_frequencies(word_dict)
wc.to_file('mount_eerie_bubble.jpg')