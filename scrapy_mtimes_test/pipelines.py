# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from scrapy_mtimes_test import settings


class ScrapyMtimesTestPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlMtimesTestPipeline(object):

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self,item,spider):
        try:
            # 插入数据
            self.cursor.execute(
                """insert into movies(movie_id,movie_name_cn, movie_name_en,movie_type,public_time,public_country,public_distributor, director,screen_writer,actors,plot,box_office,rating,hot)
                value (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (item['movie_id'],
                 item['movie_name_cn'],
                 item['movie_name_en'],
                 item['movie_type'],
                 item['public_time'],
                 item['public_country'],
                 item['public_distributor'],
                 item['director'],
                 item['screen_writer'],
                 item['actors'],
                 item['plot'],
                 item['box_office'],
                 item['rating'],
                 item['hot']
                 ))
            # print(item['name'])

            # 提交sql语句
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            # log(error)
            print('error：'+str(error.args))
        return item
