# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from WebSpider import settings
from WebSpider.items import FinanceSinaItem
from WebSpider.items import EastMoneyItem


class WebcrawlerScrapyPipeline(object):
    '''保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS finance_sina(author VARCHAR(50), title VARCHAR(255),
                               pub_time VARCHAR(50), description text, url_link text)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS east_money(author VARCHAR(50), title VARCHAR(255),
                               pub_time VARCHAR(50), description text, url_link text)""")


    # pipeline默认调用
    def process_item(self, item, spider):
        if item.__class__ == FinanceSinaItem:
            try:
                self.cursor.execute("""select * from finance_sina where url_link = %s""", item["url_link"])
                ret = self.cursor.fetchone()  #决定是更新还是首次插入
                if ret:
                    self.cursor.execute(
                        """update finance_sina set author = %s,title = %s,pub_time = %s,
                            description = %s,url_link = %s""",
                        (item['author'],
                         item['title'],
                         item['time'],
                         item['description'],
                         item['url_link']))
                else:
                    self.cursor.execute(
                        """insert into finance_sina(author,title,pub_time,description,url_link)
                          value (%s,%s,%s,%s,%s)""",
                        (item['author'],
                         item['title'],
                         item['time'],
                         item['description'],
                         item['url_link']))
                self.connect.commit()
            except Exception as error:
                print(error)
            return item

        elif item.__class__ == EastMoneyItem:
            try:
                self.cursor.execute("""select * from east_money where url_link = %s""", item["url_link"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update east_money set author = %s,title = %s,pub_time = %s,
                            description = %s,url_link = %s""",
                        (item['author'],
                         item['title'],
                         item['time'],
                         item['description'],
                         item['url_link']))
                else:
                    self.cursor.execute(
                        """insert into east_money(author,title,pub_time,description,url_link)
                          value (%s,%s,%s,%s,%s)""",
                        (item['author'],
                         item['title'],
                         item['time'],
                         item['description'],
                         item['url_link']))
                self.connect.commit()
            except Exception as error:
                print(error)
            return item

        else:
            pass