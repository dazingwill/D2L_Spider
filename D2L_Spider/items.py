# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class D2LSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ForumItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()


class TopicItem(scrapy.Item):
    id = scrapy.Field()
    forum_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class ThreadItem(scrapy.Item):
    id = scrapy.Field()
    topic_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()


class PostItem(scrapy.Item):
    id = scrapy.Field()
    thread_id = scrapy.Field()
    re_post = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()

