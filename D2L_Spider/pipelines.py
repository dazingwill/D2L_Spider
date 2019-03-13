# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.selector import Selector
from scrapy.exporters import JsonItemExporter, XmlItemExporter, JsonLinesItemExporter, CsvItemExporter

from D2L_Spider.d2l_settings import D2L_EEXPORTER_CLASS


class D2LSpiderPipeline(object):

    def __init__(self):
        self.exporters = {}

    def export(self, item):
        exporter = self.exporters[type(item).__name__]
        exporter.export_item(item)

    def open_spider(self, spider):
        for class_name in ["ForumItem", "TopicItem", "ThreadItem", "PostItem"]:
            self.exporters[class_name] = D2L_EEXPORTER_CLASS(open(class_name+".csv", "wb"))
            self.exporters[class_name].start_exporting()

    def close_spider(self, spider):
        for class_name in ["ForumItem", "TopicItem", "ThreadItem", "PostItem"]:
            self.exporters[class_name].finish_exporting()
            # self.exporters[class_name].file.close()

    def process_item(self, item, spider):
        if "content" in item:
            item["content"] = item["content"].replace('<br>', '\n')
            item["content"] = Selector(text=item["content"]).xpath("string(.)").get()
            item["content"] = item["content"].replace(u'\xa0', ' ')
        self.export(item)
        return item
