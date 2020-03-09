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
    Phone = scrapy.Field()