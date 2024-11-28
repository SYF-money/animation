# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    animation_name = scrapy.Field()
    animation_score = scrapy.Field()
    animation_edu = scrapy.Field()
    animation_zhuyan = scrapy.Field()
    animation_status = scrapy.Field()
    pass