# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from config.config import getLogConfig
from proxyPool.ProxyPoolWorker import getProxyPoolWorker

'''
    快速启动爬虫
    目的是在爬取拉勾网之前, 先爬取代理网站的代理地址
@Author monkey
@Date 2017-12-2
'''


class SpiderManager(object):

    def __init__(self):
        self.isRunning = False
        self.setting = get_project_settings()
        self.process = None

    '''
    启动 IP 代理池
    '''
    def start_proxyPool(self):
        # 启动代理
        getProxyPoolWorker().startWork()

    '''
    启动 scrapy 的爬虫程序
    '''
    def start_spider(self, spider_list):
        '''
        在同一进程里面执行多个爬虫程序
        '''
        self.process = CrawlerProcess(self.setting)
        for spider in spider_list:
            self.process.crawl(spider)
        self.process.start()

    '''
    停止爬虫和代理池
    '''
    def stop(self):
        self.isRunning = False
        # 关闭资源
        getProxyPoolWorker().stopWork()

    '''
    启动爬虫和代理池
    '''
    def start(self):
        self.start_proxyPool()
        self.start_spider()


if __name__ == '__main__':
    # 加载 Log 配置
    getLogConfig()

    manager = SpiderManager()
    # Demospider() 是 Scrapy 项目 spider 目录下的爬虫脚本名字
    # 这里需要更换成 你项目的 爬虫名
    spider_list = [Demospider(), ]
    manager.start(spider_list)
