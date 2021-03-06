# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import logging
import requests
import random
from stock.user_agents import user_agents


class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            self.logger.debug('使用代理 ' + uri)
            request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )


class RandomUserAgentMiddleware():
    def __init__(self):
        self.user_agents = user_agents


    def process_request(self, request, spider):
        user_agents = random.choice(self.user_agents)
        request.headers['User-Agent'] = user_agents
