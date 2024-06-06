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
                                     headers=self.headers,
                                     meta={"useSelenium": True,
                                           "waitTime": 20})

    def parse_product_page(self, response, **kwargs):
        # 新建产品item
        product_item = NonStopProductItem()

        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 产品详情页链接
        product_page_url = response.url

        # 获取首张预览图片链接
        # 获取id为splide01-slide01的li标签
        first_preview_pic_li_tag = soup.find('li', attrs={"id": "splide01-slide01"})
        # 找到li标签下的img标签
        first_preview_pic_tag = first_preview_pic_li_tag.find('img') if first_preview_pic_li_tag else None
        # 获取图片链接
        first_preview_pic_url = first_preview_pic_tag.get('src') if first_preview_pic_tag else ""
        first_preview_pic_url = f"https://www.nonstopdogwear.com{first_preview_pic_url}" if first_preview_pic_url and not first_preview_pic_url.startswith("https") else first_preview_pic_url


        # 获取第二张预览图片链接
        # 获取id为splide01-slide02的li标签
        second_preview_pic_li_tag = soup.find('li', attrs={"id": "splide01-slide02"})
        # 找到li标签下的img标签
        second_preview_pic_tag = second_preview_pic_li_tag.find('img') if second_preview_pic_li_tag else None
        # 获取图片链接
        second_preview_pic_url = second_preview_pic_tag.get('src') if second_preview_pic_tag else ""
        second_preview_pic_url = f"https://www.nonstopdogwear.com{second_preview_pic_url}" if second_preview_pic_url and not second_preview_pic_url.startswith("https") else second_preview_pic_url

        # 获取第三张预览图片链接
        # 获取id为splide01-slide03的li标签
        third_preview_pic_li_tag = soup.find('li', attrs={"id": "splide01-slide03"})
        # 找到li标签下的img标签
        third_preview_pic_tag = third_preview_pic_li_tag.find('img') if third_preview_pic_li_tag else None
        # 获取图片链接
        third_preview_pic_url = third_preview_pic_tag.get('src') if third_preview_pic_tag else ""
        third_preview_pic_url = f"https://www.nonstopdogwear.com{third_preview_pic_url}" if third_preview_pic_url and not third_preview_pic_url.startswith("https") else third_preview_pic_url

        # 获取产品名称
        # 获取class为Overview__Title-sc-mgw1v7-4 gEaObc的h3标签
        product_name_tag = soup.find('h3', attrs={"class": "Overview__Title-sc-mgw1v7-4 gEaObc"})
        product_name = product_name_tag.text if product_name_tag else ""

        # 获取产品类型
        # 获取class为Overview__Category-sc-mgw1v7-5 lkEogy的div标签
        product_type_tag = soup.find('div', attrs={"class": "Overview__Category-sc-mgw1v7-5 lkEogy"})
        product_type = product_type_tag.text if product_type_tag else ""

        # 产品价格
        # 获取class为itemPrice__ItemPrice-sc-7145j8-0 eKWKKD的span标签
        product_price_tag = soup.find('span', attrs={"class": "itemPrice__ItemPrice-sc-7145j8-0 eKWKKD"})
        product_price = product_price_tag.text if product_price_tag else ""

        # 产品详情
        # 获取class为Overview__Description-sc-mgw1v7-6 bvrblG的div标签
        product_details_tag = soup.find('div', attrs={"class": "Overview__Description-sc-mgw1v7-6 bvrblG"})
        product_details = product_details_tag.text if product_details_tag else ""

        # 填充item
        product_item['product_page_url'] = product_page_url
        product_item['first_preview_pic_url'] = first_preview_pic_url
        product_item['second_preview_pic_url'] = second_preview_pic_url
        product_item['third_preview_pic_url'] = third_preview_pic_url
        product_item['product_name'] = product_name
        product_item['product_type'] = product_type
        product_item['product_price'] = product_price
        product_item['product_details'] = product_details

        self.count += 1
        # logger.info(product_item)
        yield product_item

    def close(self, spider):
        logger.info(f"共爬取{self.count}个产品")
