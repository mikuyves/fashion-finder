# -*- coding: utf-8 -*-
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

def print_end():
    print 'This the end.'

if __name__ == '__main__':
    runner = CrawlerRunner(get_project_settings())

    input_url = 'http://www.lanecrawford.com/product/acne-studios/-amey-struct-v-neck-blazer-top/_/WAQ079/product.lc'
    runner.crawl('lc', url=input_url)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
