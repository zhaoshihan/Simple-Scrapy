#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
import string
import re
from WebSpider.items import FinanceSinaItem


class Spider1(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://finance.sina.com.cn/']

    def parse(self, response):
        label_list = response.xpath('//a[@target="_blank" and \
                                     re:test(@href, "http://finance.sina.com.cn/.*?/\d{4}-\d{2}-\d{2}/.*?\d+\\.shtml$") and \
                                     not(img) and \
                                     not(@href=preceding::a/@href)]') #防止重复取网址
        print(len(label_list))
        for each in label_list:
            print(each.extract())
            url = each.xpath('@href').extract_first()

            # print(url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)
            pass

    def parse_dir_contents(self, response):
        item = FinanceSinaItem()
        item['url_link'] = response.url
        # print(response.url)

        title = response.xpath('//*[@id="artibodyTitle"]/text()').extract_first().strip()
        item['title'] = title
        # print(title)

        time = response.xpath('//*[@id="wrapOuter"]/div/div[4]/span/text() | \
                               //*[@id="pub_date"]/text() | \
                               //h2[@class="u-content-time"]/text()').re_first('(\d.*\d)')
        item['time'] = time
        # print(time)

        author = response.xpath('//*[@id="wrapOuter"]/div/div[4]/span//text() |\
                                 //*[@id="media_name"]//text() |\
                                 //*[@id="author_ename"]/a/text() |\
                                 //h2[@class="u-content-time"]/text()').re_first('FX168|[\u4e00-\u9fa5][\u4e00-\u9fa5]+')
        # 这里的re匹配考虑到'FX168'不属于中文，因此单列
        # [\u4e00-\u9fa5]中文字符编码区间
        item['author'] = author
        # print(author)

        content = response.xpath('//*[@id="artibody"]//p//text()').extract()
        data1 = "".join(content)
        data2 = data1.translate(str.maketrans('', '', string.whitespace)).strip()
        final_data = re.sub("\\u3000+", "\n\n", data2)
        item['description'] = final_data
        # print(final_data)
        # print('\n')
        yield item
        pass

