# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

import time
from scrapy import signals

from scrapy_mtimes_test.settings import USER_AGENTS


class ScrapyMtimesTestSpiderMiddleware(object):
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


class ScrapyMtimesTestDownloaderMiddleware(object):
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


# 随机的User-Agent
class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)

class ProxyMiddleware(object):
    '''
    设置Proxy
    '''

    def __init__(self,ip,proxys):
        self.ip = ip
        self.proxys = proxys
        self.use_proxy = False
        self.base_time = time.time()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(ip = None,proxys=crawler.settings.get('PROXIES'))

    def process_request(self, request, spider):
        # 每隔1分钟启用一次代理
        now_time = time.time()
        duration = now_time - self.base_time
        print('当前时间分钟：--------'+str(duration))
        # 使用本地IP10秒就切换到代理
        if duration>=10*1:
            self.use_proxy = True# 标记使用代理
            print('当前代理库长度：--------' + str(len(self.proxys)))
            ip = random.choice(self.proxys)
            request.meta['proxy'] = 'http://'+ip
            print('代理：---------------------------' + request.meta['proxy'])
            # 启用代理110秒后，再切换到本机
            if duration>=60*2:
                print('---------切换到本机IP--------')
                self.use_proxy = False  # 标记关闭代理
                self.base_time = time.time()
        else:
            print('---------使用到本机IP--------')


    def process_response(self,request, response, spider):
        status = response.status
        print('-------------状态码：--------------'+str(status))
        if status!=200:
            print('-------------出错啦：---------------------------')
            if self.use_proxy:
                # error_proxy = str(request.meta['proxy'])
                # pos = error_proxy.index('/')
                # err_proxy = error_proxy[pos + 2:]  # 取出无效代理
                # print('出错无效的代理：----------------' + err_proxy)
                #
                # # self.proxys.remove(err_proxy)
                # print('出错删除了一个无效的代理：' + request.meta['proxy'] + '-------并重新选择一个代理-------')
                #
                # print('出错删除后代理库长度：-----------------' + str(len(self.proxys)))
                # raise scrapy.exceptions.IgnoreRequest
                return request
            else:
                return request

        else:
            print('-------------正常200---------------------------')
            return response


    def process_exception(self,request, exception, spider):
        return request
        # if self.use_proxy:
        #     # error_proxy = str(request.meta['proxy'])
        #     # pos = error_proxy.index('/')
        #     # err_proxy = error_proxy[pos+2:]# 取出无效代理
        #     # print('无效的代理：----------------' + err_proxy)
        #     #
        #     # # delete the error proxy from proxys list
        #     # # self.proxys.remove(err_proxy)
        #     # print('删除了一个无效的代理：'+request.meta['proxy']+'-------并重新选择一个代理-------')
        #     #
        #     # print('删除后代理库长度：-----------------'+str(len(self.proxys)))
        #     return request
