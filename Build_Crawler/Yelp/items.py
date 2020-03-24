# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    """
    items for each restaurant.
    """
    Name = scrapy.Field()
    Rating = scrapy.Field()
    Reviews = scrapy.Field()
    Price = scrapy.Field()
    Category = scrapy.Field()
    Address = scrapy.Field()
    City = scrapy.Field()
    Mon = scrapy.Field()
    Tue = scrapy.Field()
    Wed = scrapy.Field()
    Thu = scrapy.Field()
    Fri = scrapy.Field()
    Sat = scrapy.Field()
    Sun = scrapy.Field()
    Delivery = scrapy.Field()
    Wi_Fi = scrapy.Field()
    Takes_Reservations = scrapy.Field()
    Parking = scrapy.Field()
    Vegetarian_Options = scrapy.Field()
    Accepts_Credit_Cards = scrapy.Field()
    Accepts_Apple_Pay = scrapy.Field()
    Accepts_Google_Pay = scrapy.Field()
    Take_out = scrapy.Field()
    # Phone = scrapy.Field()
    # Highlights = scrapy.Field()

    def create_table(self):
        return self["Name"] == "table_start"

    def drop_exist_table_sql(self):
        """
        return the sql to drop the table in the database if the table name has been used
        """
        table_name = "yelp_" + self["City"].replace(" ", "_")
        sql = f"DROP TABLE IF EXISTS {table_name}"
        return sql

    def create_table_sql(self):
        """
        return the sql to create the table in the database with the given name
        """
        table_name = "yelp_" + self["City"].replace(" ", "_")
        sql = f"""CREATE TABLE {table_name}(
                      Name varchar(255),
                      Address varchar(255),
                      Category varchar(255),
                      Price varchar(255),
                      Rating varchar(255),
                      Reviews varchar(255),
                      Mon varchar(255),
                      Tue varchar(255),
                      Wed varchar(255),
                      Thu varchar(255),
                      Fri varchar(255),
                      Sat varchar(255),
                      Sun varchar(255),
                      Delivery varchar(255),
                      Wi_Fi varchar(255),
                      Takes_Reservations varchar(255),
                      Parking varchar(255),
                      Vegetarian_Options varchar(255),
                      Accepts_Credit_Cards varchar(255),
                      Accepts_Apple_Pay varchar(255),
                      Accepts_Google_Pay varchar(255),
                      Take_out varchar(255)
                      )"""
        return sql

    def get_insert_sql(self):
        """
        return the sql to insert the items to the table
        """
        table_name = "yelp_" + self["City"].replace(" ", "_")
        sql = f"""INSERT INTO {table_name} (Name, Address, Category, Price, Rating, Reviews, Mon, Tue, Wed, Thu, 
                              Fri, Sat, Sun, Delivery, Wi_Fi, Takes_Reservations, Parking, Vegetarian_Options, \
                              Accepts_Credit_Cards, Accepts_Apple_Pay, Accepts_Google_Pay, Take_out) 
                              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                              """
        param = (self['Name'], self['Address'], self['Category'], self['Price'],
                 self['Rating'], self['Reviews'], self['Mon'], self['Tue'], self['Wed'],
                 self['Thu'], self['Fri'], self['Sat'], self['Sun'], self['Delivery'],
                 self['Wi_Fi'], self['Takes_Reservations'], self['Parking'],
                 self['Vegetarian_Options'], self['Accepts_Credit_Cards'],
                 self['Accepts_Apple_Pay'], self['Accepts_Google_Pay'], self['Take_out'])
        return sql, param


class ReviewItem(scrapy.Item):
    """
    items for each review
    """
    Restaurant = scrapy.Field()
    City = scrapy.Field()
    Avg_rate = scrapy.Field()
    Review_rate = scrapy.Field()
    Review_time = scrapy.Field()
    Content = scrapy.Field()
    Useful = scrapy.Field()
    Funny = scrapy.Field()
    Cool = scrapy.Field()
    User_name = scrapy.Field()
    Location = scrapy.Field()
    Friend_Count = scrapy.Field()
    Review_Count = scrapy.Field()
    Total_photos = scrapy.Field()

    def create_table(self):
        return self["Restaurant"] == "table_start"

    def drop_exist_table_sql(self):
        """
        return the sql to drop the table in the database if the table name has been used
        """
        table_name = "yelp_" + self["City"].replace(" ", "_") + "_reviews"
        sql = f"DROP TABLE IF EXISTS {table_name}"
        return sql

    def create_table_sql(self):
        """
        return the sql to create the table in the database with the given name
        """
        table_name = "yelp_" + self["City"].replace(" ", "_") + "_reviews"
        sql = f"""CREATE TABLE {table_name}(
                    Restaurant varchar(255),
                    Avg_rate varchar(255),
                    Review_rate varchar(255),
                    Review_time varchar(255),
                    Content varchar(10000),
                    Useful varchar(255),
                    Funny varchar(255),
                    Cool varchar(255),
                    User_name varchar(255),
                    Location varchar(255),
                    Friend_Count varchar(255),
                    Review_Count varchar(255),
                    Total_photos varchar(255)
                    )"""
        return sql

    def get_insert_sql(self):
        """
        return the sql to insert the items to the table
        """
        table_name = "yelp_" + self["City"].replace(" ", "_") + "_reviews"
        sql = f"""INSERT INTO {table_name} (Restaurant,Avg_rate,Review_rate,Review_time,Content,Useful,
                              Funny,Cool,User_name,Location,Friend_Count,Review_Count,Total_photos) 
                              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                              """
        param = (self['Restaurant'], self['Avg_rate'], self['Review_rate'], self['Review_time'],
                 self['Content'], self['Useful'], self['Funny'], self['Cool'], self['User_name'], self['Location'],
                 self['Friend_Count'], self['Review_Count'], self['Total_photos'])
        return sql, param


