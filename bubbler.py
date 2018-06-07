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

#get average unqiue words per song
count = 0
inst_count = 0
for lyrics in me['lyrics']:
    if len(lyrics) < 30:
        inst_count += 1
    else:
        lyrics = lyrics.replace('\\n', ' ').replace("\"",'').replace('\'', '').replace('-','').replace(',', '').replace('\\','')
        lyrics = lyrics.replace('[', '').replace(']', '').replace('(','').replace(')', '').replace('/','').replace('.','').replace(':', "")
        lyrics = lyrics.lower()
        word_split = [t for t in lyrics.split()] 
        word_freq = nltk.FreqDist(word_split) 
        count += len(word_freq)
                 
avg_word_per_song = float(count)/(len(me)-inst_count)


# aggregate all lyrics togther
lyrics = ""
for i in me['lyrics']:
    lyrics = lyrics + i
 
#clean up
lyrics = lyrics.replace('\\n', ' ').replace("\"",'').replace('\'', '').replace('-','').replace(',', '').replace('\\','')
lyrics = lyrics.replace('[', '').replace(']', '').replace('(','').replace(')', '').replace('/','').replace('.','').replace(':', "")
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
            'of', 'was', 'it', 'that', 'not', 'theres', 'verse', 'chorus'
            '1', '2', '3', 'dont', 'ill', 'doo', 'intro', 'outro', 'be', 
            'are', '15', 'john', 'lennon', 'paul', 'mccartney', '&', 'chorus',
            'can', 'got', 'kendrick', 'cash', 'get', 'one', 'id','on',
            'by', 'nigga', 'niggas', 'hook', 'chance', 'rapper', 'lamar',
            'instrumental', '4', '5', '6', '7' ,'8', '9', '10', 'pharrell',
            'teddy', 'kanye', 'west', 'tit', 'hranica', 'jeremy', 'mike',
            'depoyster']
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
#print(lemmatizer.lemmatize('died')) 

#bubbler
color_map = raw_input('enter colormap: ')
background = raw_input('enter background color: ')
wc = WordCloud(height = 500, width = 1000, background_color=background, max_words=2000,
               stopwords=stopwords, max_font_size=175, random_state=42, relative_scaling = .4,
               colormap = color_map)

wc = wc.generate_from_frequencies(word_dict)
wc.to_file('imgs/' + artist + '_bubble.jpg')


print('Avg. Unique Words per Song: ')
print(avg_word_per_song)
print('Unique word count: ')
print(float(len(freq))/len(cleaned_words) *100)