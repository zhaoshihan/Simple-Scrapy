#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import etree
import string

html = '''
<book>
    <author>Tom <em>John</em> cat</author>
    <author>Jerry <em>Bush</em> mouse</author>
    <pricing>
        <price>20</price>
        <discount>0.8</discount>
    </pricing>
</book>
'''

selector = etree.HTML(html)
data = selector.xpath('//book/author/text()')
# print(data)
str1 = " ".join(data)
# print(str1)

data2 = selector.xpath('string(//book//author)')
# print(data2)


# intab = "aeiou"
# outtab = "12345"
trantab = str.maketrans(" ", "\n")

str = "this is string example......wow,  yeah!"
print(str.translate(trantab).strip())
