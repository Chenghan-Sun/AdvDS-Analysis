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
        if item.create_table():
            self.cursor.execute(item.drop_exist_table_sql())
            self.cursor.execute(item.create_table_sql())
            self.conn.commit()
        else:
            insert_sql, param = item.get_insert_sql()
            self.cursor.execute(insert_sql, param)
            self.conn.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()