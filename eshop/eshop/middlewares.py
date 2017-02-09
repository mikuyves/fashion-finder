# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import logging
from urlparse import urlparse

from scrapy.http import Request
from scrapy.utils.python import WeakKeyCache
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


logger = logging.getLogger(__name__)


class RotateUserAgentMiddleware(UserAgentMiddleware):
    """Avoiding baned. This script is from coolscrapy by yidao620c, url as follow:
https://github.com/yidao620c/core-scrapy/blob/master/coolscrapy/middlewares.py
    """
    def __init__(self, user_agent=''):
        super(RotateUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            # Record current UserAgent.
            logger.debug('Current UserAgent: ' + ua)
            request.headers.setdefault('User-Agent', ua)

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more visit http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]


PROXIES = [
    '12.129.82.194:8080',
    '158.69.172.98:80',
    '54.172.126.149:8083',
]


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        try:
            request.meta['rule']['proxy']
            proxy = random.choice(PROXIES)
            print "{0:*>50} => {1:*<50}".format('ProxyMiddleware', proxy)
            request.meta['proxy'] = "http://%s" % proxy
        except KeyError as e:
            pass


class GoogleCacheMiddleware(object):
    """This middleware allow spider to crawl the spicific domain url in google
    caches. You can define the GOOGLE_CACHE_DOMAINS in settings,it is a list
    which you want to visit the google cache.Or you can define a google_cache_domains
    in your spider and it is as the highest priority.
    """
    google_cache = 'http://webcache.googleusercontent.com/search?q=cache:'

    def __init__(self, cache_domains=''):
        self.cache = WeakKeyCache(self._cache_domains)
        self.cache_domains = cache_domains

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings['GOOGLE_CACHE_DOMAINS'])

    def _cache_domains(self, spider):
        if hasattr(spider, 'google_cache_domains'):
            return spider.google_cache_domains
        elif self.cache_domains:
            return self.cache_domains

        return ""

    def process_request(self, request, spider):
        """The scrapy documention said that:
	If it returns a Request object, the returned request will be rescheduled
        (in the Scheduler) to be downloaded in the future. The callback of the
        original request will always be called. If the new request has a callback
        it will be called with the response downloaded, and the output of that
        callback will then be passed to the original callback. If the new request
        doesn’t have a callback, the response downloaded will be just passed to
        the original request callback. But actually is that if it returns a Request
        object,then the original request will be droped,so you must make sure
        that the new request object's callback is the original callback.
	"""
        gcd = self.cache[spider]
        if gcd:
            if urlparse(request.url).netloc in gcd:
                request = request.replace(url=self.google_cache + request.url)
                #request = Request(self.google_cache + request.url,request.callback)
                request.meta['google_cache'] = True
                return request

    def process_response(self, request, response, spider):

        if request.meta.get('google_cache',False):
            return response.replace(url = response.url[len(self.google_cache):])

        return response
