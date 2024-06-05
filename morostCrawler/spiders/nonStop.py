# -*- coding: utf-8 -*- 
# @Time: 2024/6/5 下午10:44 
# @Author: morost
# @File: nonStop.py 
# @desc: https://www.nonstopdogwear.com/en/for-dogs/
# scrapy crawl nonStop --nolog

import re
import math
import scrapy
from loguru import logger
from bs4 import BeautifulSoup

from scrapy.utils.project import get_project_settings

from morostCrawler.items.nonStop import NonStopProductItem


# NonStop 产品爬虫-----------------------------------------------------------------------------------------------------
class NonStopSpider(scrapy.Spider):
    name = "nonStop"
    allowed_domains = ["nonstopdogwear.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取链接
        self.start_url = "https://www.nonstopdogwear.com/en/for-dogs/"
        # 产品计数
        self.count = 0
        # 产品总数
        self.product_total_num = 0
        logger.info(f"NonStopSpider {self.start_url}")

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,
                             callback=self.parse,
                             headers=self.headers)

        # yield scrapy.Request(url=self.start_url,
        #                      callback=self.parse,
        #                      headers=self.headers,
        #                      meta={"useSelenium": True,
        #                            "rollDown": True})

    def parse(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # print(soup)

        # 获取产品列表区域标签
        products_grid_upper_tag = soup.find('h3', attrs={"id": "products"})
        products_grid_tag = products_grid_upper_tag.find_next('div')

        if products_grid_tag:
            # 获取所有产品详情页链接tag
            product_info_link_tags = products_grid_tag.find_all('a', recursive=False)

            # 循环爬取每一个产品详情页链接
            for product_info_link_tag in product_info_link_tags:
                product_info_url = product_info_link_tag.get('href')
                product_info_url = f"https://www.nonstopdogwear.com{product_info_url}" if not product_info_url.startswith("https") else product_info_url

                print(product_info_url)

                yield scrapy.Request(url=product_info_url,
                                     callback=self.parse_product_page,
                                     headers=self.headers)

    def parse_product_page(self, response, **kwargs):
        # 新建产品item
        product_item = NonStopProductItem()

        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 产品详情页链接
        product_page_url = response.url
