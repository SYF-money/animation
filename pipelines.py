# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AnimationPipeline:
    connect = pymysql.connect(host='localhost',port=3306,user='root',
                              passwd='',db='animation',charset='utf8')
    def process_item(self, item, spider):
        sql = "insert into animations values(%s,%s,%s,%s,%s)"
        cursor = self.connect.cursor()
        cursor.execute(sql, (item['animation_name'], item['animation_score'],
                             item['animation_edu'], item['animation_zhuyan'],
                             item['animation_status']))
        self.connect.commit()
        return item
