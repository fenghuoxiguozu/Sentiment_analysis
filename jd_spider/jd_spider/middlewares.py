# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .spiders.model import ProxyModel
from twisted.internet.defer import DeferredLock



class JdSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JdSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


import random
from scrapy import signals
import requests
import time,json
# from jd_spider.settings import IPPOOL




class MyproxiesSpiderMiddleware(object):
    PROXY_URL='http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=100&pro=&city=&port=1&format=json&ss=5&css=&et=1&dt=1&specialTxt=3&specialJson='
    # PROXY_URL ='http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=95bb17f557364f2992809dbcd1d0b22e&orderno=YZ20195269124eDlpnB&returnType=2&count=1'
    validate_url = 'https://www.baidu.com/'

    def __init__(self):
        super(MyproxiesSpiderMiddleware,self).__init__()
        self.current_proxy=None
        self.lock=DeferredLock()

    def process_request(self,request,spider):
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            self.update_proxy()
        request.meta["proxy"] = self.current_proxy.proxy

    def process_response(self,request,response,spider):
        res=requests.get(url=self.validate_url)
        if res.status_code !=200:
        # if response.status != 200:
            self.update_proxy()
            return request
        return response

    def update_proxy(self):
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expiring:
            text=requests.get(self.PROXY_URL).text
            result=json.loads(text)
            # print(result)
            if len(result['data'])>0:
                data=result['data'][0]
                print('重新获取一个代理：', data)
                proxy_model=ProxyModel(data)
                self.current_proxy=proxy_model
        self.lock.release()








