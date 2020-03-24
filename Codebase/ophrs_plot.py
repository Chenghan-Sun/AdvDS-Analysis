import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
plt.style.use('ggplot')
import seaborn as sns
from helper_fe import *


class OpHrsPlot:
    
    def __init__(self, df):
        self.df = df
        
    def add_hours_feature(self):
        """ add 14 new features about open and close time for all restaurants in given dataframe 
        based on original weekdays features
        """
        self.df[['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 
            'Sun']] = self.df[['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']].applymap(get_open_time)
        self.df[['MonOpen', 'TueOpen', 'WedOpen', 'ThuOpen', 'FriOpen', 'SatOpen',
            'SunOpen']] = self.df[['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']].applymap(grab_start_open)
        self.df[['MonClose', 'TueClose', 'WedClose', 'ThuClose', 'FriClose', 'SatClose',
            'SunClose']] = self.df[['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']].applymap(grab_end_open)
        return self.df
    
    def box_plot(self, font_size, title):
        """ make ratings distribution plot
        for open hours analysis 
        """
        clean_df_sub = self.df[['MonOpen', 'TueOpen', 'WedOpen', 'ThuOpen', 'FriOpen', 'SatOpen', 'SunOpen']]
        ax = sns.boxplot(data=clean_df_sub)
        plt.title(title, fontsize=font_size)
        plt.xlabel("Operation Hours", fontsize=font_size)
        plt.ylabel("Week days", fontsize=font_size)
    
    def violin_plot(self, font_size, title):
        """ make ratings distribution plot 
        for close hours analysis 
        """
        clean_df_sub = self.df[['MonClose', 'TueClose', 'WedClose', 'ThuClose', 'FriClose', 'SatClose', 'SunClose']]
        ax = sns.violinplot(data=clean_df_sub)
        plt.title(title, fontsize=font_size)
        plt.xlabel("Operation Hours", fontsize=font_size)
        plt.ylabel("Week days", fontsize=font_size)
