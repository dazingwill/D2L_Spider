# -*- coding: utf-8 -*-
import re

import scrapy
import browser_cookie3
from scrapy.exceptions import CloseSpider

from D2L_Spider.items import TopicItem, ThreadItem, ForumItem, PostItem
from D2L_Spider.d2l_settings import D2L_DISCUSSION_URL


class TopicSpider(scrapy.Spider):
    name = 'topic'
    allowed_domains = ['courses.uscden.net']

    def start_requests(self):
        url = D2L_DISCUSSION_URL
        cookies = browser_cookie3.load('.uscden.net')
        cookies_dict = {cookie.name: cookie.value for cookie in cookies}
        return [scrapy.Request(url, cookies=cookies_dict, callback=self.parse_forum)]

    def parse_forum(self, response):

        # check if login successful
        if response.xpath("//title/text()").get() is None:
            self.log("cannot login, please check chrome cookies")
            return

        # discussion list
        forum_items = response.xpath("//div[@data-forum-id]")
        for forum_item in forum_items:
            forum_id = forum_item.attrib["data-forum-id"]
            forum_item = forum_item.xpath("..")
            title = forum_item.xpath(".//h2/text()").get()
            yield ForumItem(id=forum_id, title=title)

            # parse topic list
            topic_elems = forum_item.xpath(".//div[starts-with(@id,'topicDetailsPlaceholderId')]/h3/a")
            for a in topic_elems:
                title = a.xpath("text()").get()
                url = response.urljoin(a.attrib["href"])
                id = re.search("(?<=/topics/)\d+", url).group(0)
                yield TopicItem(id=id, forum_id=forum_id, title=title, url=url)
                yield scrapy.Request(url=url, callback=self.parse_topic, meta={"topic_id": id})

    def parse_topic(self, response):
        # not able to find any topic with more pages, so for now only parse the first page
        thread_elems = response.xpath("//div[starts-with(@id,'threadListItemContents_')]//h2/a")
        for a in thread_elems:
            url = response.urljoin(a.attrib["href"])
            yield scrapy.Request(url=url, callback=self.parse_thread, meta=response.meta)


    def parse_thread(self, response):
        url = response.url
        title = response.xpath("//h1/text()").get()
        thread_id = re.search("(?<=/threads/)\d+", url).group(0)
        topic_id = response.meta["topic_id"]

        statuses_item = response.xpath("//div[@class=' d2l-thread-statuses-container']/div/text()").get().split(" posted ")
        author = statuses_item[0]
        time = statuses_item[1]
        content = response.xpath("string(//div[@class='d2l-htmlblock d2l-htmlblock-deferred d2l-htmlblock-untrusted'])").get()
        yield ThreadItem(id=thread_id, topic_id=topic_id, title=title, url=url, author=author, time=time, content=content)

        # Posts in this thread

        last_posts = ["-1", "-1", "-1", "-1"]
        post_items = response.xpath("//div[@data-postid]")
        for post_item in post_items:

            post_id = post_item.attrib["data-postid"]

            author = post_item.xpath(".//*[starts-with(name(),'h') and string-length(name())=2]")
            if not author:
                raise CloseSpider("cannot find author of the post" + url)
            level = int(author.xpath("name()").get()[1])-2
            last_posts[level] = post_id
            author = author.xpath("./text()").get()

            re_post = "-1" if level > 0 else last_posts[level-1]

            time = post_item.xpath(".//abbr").attrib["title"]
            content = post_item.xpath(
                ".//div[@class='d2l-htmlblock d2l-htmlblock-deferred d2l-htmlblock-untrusted']").get()
            yield PostItem(id=post_id, thread_id=thread_id, re_post=re_post, author=author, time=time, content=content)

    def parse(self, response):
        pass
