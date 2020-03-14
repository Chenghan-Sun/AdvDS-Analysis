# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
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
    Health_Score = scrapy.Field()
    Wi_Fi = scrapy.Field()
    Smoking = scrapy.Field()
    Delivery = scrapy.Field()
    Take_out = scrapy.Field()
    # Phone = scrapy.Field()
    # Highlights = scrapy.Field()
