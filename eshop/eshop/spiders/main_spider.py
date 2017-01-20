# -*- coding: utf-8 -*-
import os

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings



if __name__ == '__main__':
    runner = CrawlerRunner(get_project_settings())
    from eshop.settings import PROJECT_PATH

    with open(os.path.join(PROJECT_PATH, 'urls.txt')) as f:
        urls = f.read().split('\n')
    runner.crawl('lc', urls=urls)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
