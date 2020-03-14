# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
import pymysql


class DefaultValuesPipeline(object):

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, 'NULL')
        return item


class YelpPipeline(object):
    def process_item(self, item, spider):
        return item


class CsvPipeline(object):

    def __init__(self):
        self.file = open("Yelp_davis.csv",'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', '12345678', 'yelp_db')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        table_name = "yelp_" + item["City"].replace(" ", "_")
        if item["Name"] == "table_start":
            self.create_table(table_name)
            return item
        insert_sql = f"""INSERT INTO {table_name} (Name, Address, Category, Price, Rating, Reviews, Mon, Tue, Wed, Thu, 
                      Fri, Sat, Sun, Health_Score, Wi_Fi, Smoking, Delivery, Take_out) 
                      VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                      """
        self.cursor.execute(insert_sql, (item['Name'], item['Address'], item['Category'], item['Price'],
                                         item['Rating'], item['Reviews'], item['Mon'], item['Tue'], item['Wed'],
                                         item['Thu'], item['Fri'], item['Sat'], item['Sun'], item['Health_Score'],
                                         item['Wi_Fi'], item['Smoking'], item['Delivery'], item['Take_out']))
        self.conn.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def create_table(self, table_name):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
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
              Health_Score varchar(255),
              Wi_Fi varchar(255),
              Smoking varchar(255),
              Delivery varchar(255),
              Take_out varchar(255)
              )"""
        self.cursor.execute(sql)
        self.conn.commit()



