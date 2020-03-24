import pandas as pd
import matplotlib.pyplot as plt
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
plt.style.use('ggplot')
import seaborn as sns
from helper_fe import *


class RatdistPlot:
    
    def __init__(self, df):
        self.df = df
        
    @staticmethod
    def plot(clean_df, font_size, title):
        """ make ratings distribution plot 
        """
        x_axis = clean_df['Rating'].value_counts()
        if "Unknown" in x_axis:
            x_axis.pop("Unknown")
        x_axis = x_axis.sort_index()
        ax = sns.barplot(x_axis.index, x_axis.values, alpha=0.8)
        plt.title(title, fontsize=font_size)
        plt.xlabel("Restaurants Ratings", fontsize=font_size)
        plt.ylabel("Rating Counts", fontsize=font_size)

        # adding the text labels
        rects = ax.patches
        labels = x_axis.values
        for rect, label in zip(rects, labels):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')
            
    def clean_each_city_df(self):
        """ helper function of `ratdist_plot`
        data cleaning ensemble for each yelp city dataframe 
        """
        exceptions(self.df)
        clean_df = self.df.applymap(find_null)
        return clean_df
