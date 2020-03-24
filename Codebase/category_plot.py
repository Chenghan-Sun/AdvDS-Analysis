import pandas as pd
import sys
import numpy as np
import os
import nltk
import string
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
plt.style.use('ggplot')
from wordcloud import WordCloud 
import seaborn as sns
from helper_fe import *


class CategoryPlot(object):
    
    def __init__(self, data, remove=string.punctuation):
        self.pattern = fr"[{remove}]"
        self.cat_frequency = {}
        self.data = data
        
    def _regex_split_join(self, item):
        """ statistics on word frequency by attributes
        """
        try:
            to_be_join = re.split(self.pattern, item.strip())
        except:
            raise Exception(f'the item --{item} in the line above is not a string')
        for word in to_be_join:
            new_word = word.strip()
            if new_word in self.cat_frequency:
                self.cat_frequency[new_word] += 1
            else:
                self.cat_frequency[new_word] = 1
        return " ".join(to_be_join)
    
    def category_counting(self):
        """ apply count frequency
        """
        self.data[['Category']].applymap(self._regex_split_join)  # deep copy
        del self.cat_frequency['Unknown']  # drop the "Unknown" case
        if '' in self.cat_frequency:
            del self.cat_frequency['']  # drop the "" case
        return self.cat_frequency
    
    def cat_plot(self, num_top, font_size, title, overall=False, verbose=False):
        """ Frequency bar plot 
        """
        catfre_df = pd.DataFrame(self.cat_frequency.items(), columns=['Word_Categories', 'Frequency'])
        # sort the df by word frequency 
        catfre_df = catfre_df.sort_values('Frequency', ascending=False)
        tot_cat = catfre_df.Word_Categories.value_counts()
        if verbose:
            print(f"There are {len(tot_cat)} different word categories to describe restaurants in Yelp")

        top_cat = catfre_df.Word_Categories.iloc[0:num_top]
        top_fre = catfre_df.Frequency.iloc[0:num_top]
        if overall:
            plt.figure(figsize=(20, 14))
        ax = sns.barplot(top_fre.values, top_cat.values, alpha=0.8)
        plt.title(title, fontsize=font_size)
        #locs, labels = plt.xticks()
        #plt.setp(labels, rotation=90)
        plt.ylabel('Word Categories', fontsize=font_size)
        plt.xlabel('Word Frequency', fontsize=font_size)

        # adding the text labels
        rects = ax.patches
        labels = top_fre.values
        for rect, label in zip(rects, labels):
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()+5, height/2+rect.get_y(), label, ha='left')
            
    def make_word_cloud(self, text, max_word=30):
        """ generate word cloud by word frequency
        """
        wordcloud = WordCloud(
            background_color='white',
            stopwords=stopwords.words("english"),
            scale=10,
            max_words=max_word,
            max_font_size=40)
        wordcloud = wordcloud.generate_from_frequencies(frequencies=self.cat_frequency)
        plt.figure(1,figsize=(15,15))
        plt.axis('off')
        plt.imshow(wordcloud, interpolation="bilinear") 
