#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
import string
import re

from WebSpider.items import EastMoneyItem


class Spider2(scrapy.Spider):
    name = 'spider2'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://www.eastmoney.com/']

    def parse(self, response):
        label_list = response.xpath('//a[re:test(@href, "http://.*?(?<!ideo|life)\\.eastmoney.com/news/\d+,\d+\\.html") and \
                                     not (img)]') #去除财经生活、视频类报道
        print(len(label_list))
        for each in label_list:
            print(each.extract())
            # url_old = each.xpath('@href').extract_first()
            url = each.xpath('@href').re_first('(.*)\\.html') + "_0.html" #这里照顾到翻页无法取全文的问题，故用_0.html取全文网页
            # print(url_old)
            # print(url)
            # print('\n')
            yield scrapy.Request(url, callback=self.parse_dir_contents)
            pass

    def parse_dir_contents(self, response):
        item = EastMoneyItem()
        item['url_link'] = response.url

        title = response.xpath('//h1/text()').extract_first().strip()
        item['title'] = title

        time = response.xpath('//div[@class="time"]/text()').extract_first()
        item['time'] = time

        author = response.xpath('//div[@class="source"]/img/@alt |\
                                 //div[@class="source"]/a/text()').extract_first()
        item['author'] = author

        content = response.xpath('//div[@id="ContentBody"]/p/text() |\
                                  //div[@id="ContentBody"]//a[@class]/text() |\
                                  //div[@id="ContentBody"]/p/strong/text() |\
                                  //div[@id="ContentBody"]/text()').extract()
        data1 = "".join(content)
        data2 = data1.translate(str.maketrans('', '', string.whitespace)).strip() #string.whitespace = ' \t\n\r\v\f'
        final_data = re.sub("\\u3000+", "\n\n", data2)
        # print(title)
        # print(response.url)
        # print(final_data)
        # print('\n')
        item['description'] = final_data
        yield item
        pass
