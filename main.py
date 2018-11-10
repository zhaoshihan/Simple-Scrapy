#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapy import cmdline

# cmdline.execute("scrapy crawl spider1".split())
cmdline.execute("scrapy crawl spider1 -o FinanceSinaItems.csv -t csv --nolog".split())

# cmdline.execute("scrapy crawl spider2 --nolog".split())
# cmdline.execute("scrapy crawl spider2 -o EastMoneyItems.csv -t csv --nolog".split())


