# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from twisted.enterprise import adbapi
import pymysql
from pymysql import cursors

class JdSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    def __init__(self):
        dbparms={
            'host': settings['MYSQL_HOST'],
            'port': settings['MYSQL_PORT'],
            'user' :settings['MYSQL_USER'],
            'password' : settings['MYSQL_PASSWORD'],
            'database' : settings['MYSQL_DBNAME'],
            'charset' : 'utf8',
            'cursorclass':cursors.DictCursor
        }
        self.dbpool=adbapi.ConnectionPool('pymysql',**dbparms)

    def process_item(self,item,spider):
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,spider)

    def handle_error(self,failure,spider):
        print(failure)

    def do_insert(self,cursor,item):
        item_data = (item['id'], item['content'], item['nickname'], item['score'])
        sql = "insert IGNORE into jd_comment(id,content,nickname,score)VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,item_data)