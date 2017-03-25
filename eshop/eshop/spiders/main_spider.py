# -*- coding: utf-8 -*-
import os
import re
import logging
import logging.config

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings


if __name__ == '__main__':
    runner = CrawlerRunner(get_project_settings())

    # Set logger.
    from eshop.settings import PROJECT_PATH
    logging.config.fileConfig(os.path.join(PROJECT_PATH, 'log.conf'))
    logger = logging.getLogger('eshop')

    # Get URLs in the file.
    with open(os.path.join(PROJECT_PATH, 'urls.txt')) as f:
        urls = f.read().split('\n')
        urls = [re.sub(r'\?\S+$', '', url) for url in urls if url]

    # Start.
    runner.crawl('lc', urls=urls)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
