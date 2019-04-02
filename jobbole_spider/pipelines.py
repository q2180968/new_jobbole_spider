# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import json
import codecs
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


# 原生pipeline
class JobboleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 获取图片地址
class ArticlePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'front_image_url' in item:
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
            # 一定要将item返回回去
        return item


# json保存pipeline
class JsonSavePipeline(object):
    def __init__(self):
        self.json_file = codecs.open('AtricleJson.json', 'w', encoding='UTF-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.json_file.write(lines)
        return item

    def close_spider(self, spider):
        print('spiderclose')
        self.json_file.close()


# json导出pipeline
class jsonExporterPipeline(object):
    def __init__(self):
        self.file = open('ArticlaExporterJson.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# mysql插入数据
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '50122294', 'jobbole_spider', charset='utf8mb4',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = '''
            insert into jobbole_article(title,create_date,url,url_object_id,content,comment_nums,fav_nums,praise_nums,tag,front_image_url,front_image_path)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        self.cursor.execute(insert_sql, (
            item['title'], item['create_date'], item['url'], item['url_obj_id'], item['content'], item['comment_nums'],
            item['fav_nums'], item['praise_nums'],
            ','.join(item['tags']), item['front_image_url'], item['front_image_path']))
        self.conn.commit()

        def close_spider(self, spider):
            self.conn.close()


class MysqlTwistedPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PWD'],
            charset='utf8mb4',
            use_unicode=True,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **db_params)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        # 使用twisted将mysql变成异步操作
        query = self.dbpool.runInteraction(self.do_insert, item)

        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = '''
                    insert into jobbole_article(title,create_date,url,url_object_id,content,comment_nums,fav_nums,praise_nums,tag,front_image_url,front_image_path)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                '''
        cursor.execute(insert_sql, (
            item['title'], item['create_date'], item['url'], item['url_obj_id'], item['content'], item['comment_nums'],
            item['fav_nums'], item['praise_nums'],
            ','.join(item['tags']), item['front_image_url'], item['front_image_path']))
