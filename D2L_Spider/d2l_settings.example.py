# -*- coding: utf-8 -*-
from scrapy.exporters import JsonItemExporter, XmlItemExporter, JsonLinesItemExporter, CsvItemExporter

# The URL of discussion page you want to crawl
# https://courses.uscden.net/d2l/le/{discussion id}/discussions/List
D2L_DISCUSSION_URL = "https://courses.uscden.net/d2l/le/12345/discussions/List"

# The formats of result files
# See https://docs.scrapy.org/en/latest/topics/exporters.html
D2L_EEXPORTER_CLASS = CsvItemExporter
