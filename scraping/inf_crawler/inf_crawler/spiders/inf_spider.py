import os
import json
import uuid
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

PATH = "documents/"


class InfSpider(CrawlSpider):
    name = "inf_spider"
    allowed_domains = ['inf.ed.ac.uk']
    start_urls = ['http://course.inf.ed.ac.uk/']  
    
    rules = (
        # crawl all "teaching/courses" webpages, ignore those that are not html/py/txt files
        Rule(LinkExtractor(allow=(r'teaching/courses/.*',),
            deny=(r'/teaching/courses/.*\.(?!py|txt|html).*',)), 
            callback='parse_pages', follow=True),
        # get all course webpages from main portal
        Rule(LinkExtractor(allow=(r'^http://course\.inf\.ed\.ac\.uk/.*$',), deny=(r'.*cgi-bin.*', r'.*\.shtml')),
        follow= True),
    )


    def parse_pages(self, response):
        """ Save each crawled webpage as a json file. """

        # a py/txt page (does not have a <body>, or <title>)
        if response.url.split(".")[-1] in ["py","txt"]:
            title = response.url.split("/")[-1]
            content = map(lambda x: x.strip(), response.body.split())
            content = filter(lambda x: x != '', content)
            content = " ".join(str(content))
        else:
            title = response.xpath('//head/title/text()').extract_first()
            content = ""
            # extract all text, except for js scripts from the page
            for tag in response.xpath('//body/descendant-or-self::*[not(self::script)]/text()').extract():
                tag = map(lambda x: x.strip(), tag.split())
                tag = filter(lambda x: x != '', tag)
                if tag:
                    content += (" " + " ".join(tag))

        data = {'title': title,
                'content': content,
                'type' : 'page',
                'url'  : response.url
                }

        # generate uuid as filename
        filename = str(uuid.uuid4()) + ".json"
        # make sure that it didn't accidentally generate a pre-existing random uuid...
        while os.path.isfile(PATH + filename):
            filename = str(uuid.uuid4()) + ".json"

        with open(PATH + filename, 'w', encoding="utf8") as f:
            json.dump(data, f)
