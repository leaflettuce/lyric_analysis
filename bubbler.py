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
artist = str(raw_input('enter artist name: (ex: mount_eerie): '))
me = pd.read_csv("data/" + artist + ".csv")

# aggregate all lyrics togther
lyrics = ""
for i in me['lyrics']:
    lyrics = lyrics + i
 
#clean up
lyrics = lyrics.replace('\\n', ' ').replace("\"",'').replace('\'', '').replace('-','').replace(',', '').replace('\\','')
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

del_words = ['the', 'and', 'i', 'a', 'in', 'my', 'your', 'to', 'but', 'go',
             'i\m', 'im','with','to','so','this','is','you','me','see','do','the',
            'of', 'was', 'it', 'that', 'not', 'theres', 'verse', 'chorus',
            '1', '2', '3', 'dont', 'ill', 'doo', 'intro', 'outro', 'be', 
            'are', '15']
for i in del_words:
    if i in word_dict.keys():
        del word_dict[i]


# plot
words_listed = sorted(word_dict.items())
x, y = zip(*words_listed)
plt.plot(x, y)
plt.show()


#lemmatize
lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize('died')) 

#bubbler
color_map = raw_input('enter colormap: ')
background = raw_input('enter background color: ')
wc = WordCloud(height = 500, width = 1000, background_color=background, max_words=2000,
               stopwords=stopwords, max_font_size=170, random_state=42, relative_scaling = .5,
               colormap = color_map)

wc = wc.generate_from_frequencies(word_dict)
wc.to_file('imgs/' + artist + '_bubble.jpg')

print('Unique word count: ')
print(float(len(freq))/len(cleaned_words) *100)