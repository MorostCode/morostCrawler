# -*- coding: utf-8 -*- 
# @Time: 2024/5/28 下午11:26 
# @Author: morost
# @File: toyFox.py 
# @desc: https://cloakanddawggie.com/collections/all
# scrapy crawl toyFox --nolog

import scrapy
from loguru import logger
from bs4 import BeautifulSoup

from scrapy.utils.project import get_project_settings

from morostCrawler.items.toyFox import ToyFoxProductItem


# ToyFox 产品爬虫--------------------------------------------------------------------------------------------------------
class ToyFoxSpider(scrapy.Spider):
    name = "toyFox"
    allowed_domains = ["cloakanddawggie.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取链接
        self.start_url = "https://cloakanddawggie.com/collections/all"
        # 产品计数
        self.count = 0
        logger.info(f"ToyFoxSpider {self.start_url}")

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,
                             callback=self.parse,
                             headers=self.headers)

    # 解析产品主页
    def parse(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取页码区域标签
        pagination_tag = soup.find('div', attrs={"class": "pagination"})
        # 获取所有的span标签（一级标签）
        span_tags = pagination_tag.find_all("span", attrs={"class": "page"})
        # 获取“最后一页”按钮标签
        last_page_tag = span_tags[-1] if span_tags else None
        # 获取“最后一页”按钮的a标签
        last_page_a_tag = last_page_tag.find('a') if last_page_tag else None
        # 获取最后一页的页码
        last_page_num = int(last_page_a_tag.text) if last_page_a_tag else 1

        # 循环爬取每一页
        for i in range(1, last_page_num + 1):
            # 拼接url
            page_url = f"{self.start_url}?page={i}"
            yield scrapy.Request(url=page_url,
                                 callback=self.parse_product_list_page,
                                 headers=self.headers)

    # 解析产品列表页
    def parse_product_list_page(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取产品列表区域标签
        product_list_tag = soup.find('div', attrs={"class": "grid grid--uniform"})

        if product_list_tag:
            # 获取产品标签列表
            product_tags = product_list_tag.find_all('div', attrs={"data-aos": "row-of-4"})

            # 循环爬取每一个产品
            for product_tag in product_tags:
                # 获取产品信息tag
                product_info_tag = product_tag.find('div', attrs={"class": "grid-product__content"})
                # 获取产品详情页链接
                product_page_url_tag = product_info_tag.find('a', attrs={"class": "grid-product__link"})
                product_page_url = product_page_url_tag.get('href') if product_page_url_tag else ""
                product_page_url = f"https://cloakanddawggie.com/{product_page_url}" if not product_page_url.startswith("https://cloakanddawggie.com/") else product_page_url

                # 请求产品详情页
                yield scrapy.Request(url=product_page_url,
                                     callback=self.parse_product_page,
                                     headers=self.headers)

    # 解析产品详情页
    def parse_product_page(self, response, **kwargs):
        # 新建产品item
        product_item = ToyFoxProductItem()

        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 产品详情页链接
        product_page_url = response.url

        # 获取首张预览图链接
        first_preview_tag = soup.find('div', attrs={"class": "product__thumb-item", "data-index": "0"})
        first_preview_a_tag = first_preview_tag.find('a') if first_preview_tag else None
        first_preview_pic_url = first_preview_a_tag.get('href') if first_preview_tag else ""
        first_preview_pic_url = f"https:{first_preview_pic_url}" if first_preview_tag and not first_preview_pic_url.startswith("https:") else first_preview_pic_url
        # 如果首张预览图为空，则用另一种方法获取
        if not first_preview_pic_url:
            first_preview_tag = soup.find('div', attrs={"class": "product-image-main"})
            first_preview_pic_tag = first_preview_tag.find('img') if first_preview_tag else None
            first_preview_pic_url = first_preview_pic_tag.get('data-photoswipe-src') if first_preview_pic_tag else ""
            first_preview_pic_url = f"https:{first_preview_pic_url}" if first_preview_tag and not first_preview_pic_url.startswith("https:") else first_preview_pic_url

        # 获取第二张预览图链接
        second_preview_tag = soup.find('div', attrs={"class": "product__thumb-item", "data-index": "1"})
        second_preview_a_tag = second_preview_tag.find('a') if second_preview_tag else None
        second_preview_pic_url = second_preview_a_tag.get('href') if second_preview_tag else ""
        second_preview_pic_url = f"https:{second_preview_pic_url}" if second_preview_tag and not second_preview_pic_url.startswith("https:") else second_preview_pic_url

        # 获取第三张预览图链接
        third_preview_tag = soup.find('div', attrs={"class": "product__thumb-item", "data-index": "2"})
        third_preview_a_tag = third_preview_tag.find('a') if third_preview_tag else None
        third_preview_pic_url = third_preview_a_tag.get('href') if third_preview_tag else ""
        third_preview_pic_url = f"https:{third_preview_pic_url}" if third_preview_tag and not third_preview_pic_url.startswith("https:") else third_preview_pic_url

        # 产品名称
        product_name_tag = soup.find('h1', attrs={"class": "product-single__title"})
        product_name = product_name_tag.text if product_name_tag else ""
        product_name = product_name.replace("\n", "") if product_name else ""

        # 产品价格
        product_price_tag = soup.find('span', attrs={"class": "product__price"})
        product_price = product_price_tag.text if product_price_tag else ""
        product_price = product_price.replace("\n", "") if product_price else ""
        # 如果产品价格为空，则用另一种方法获取
        if not product_price:
            product_price_tag = soup.find('span', attrs={"class": "product__price on-sale"})
            product_price = product_price_tag.text if product_price_tag else ""
            product_price = product_price.replace("\n", "") if product_price else ""

        # 产品描述
        product_text_info_tag = soup.find('div', attrs={"class": "rte"})

        # 产品描述（主要）
        description_main_upper_tag = product_text_info_tag.find('h2') if product_text_info_tag else None
        description_main_tag = description_main_upper_tag.find('span') if description_main_upper_tag else None
        product_description_main = description_main_tag.text if description_main_tag else ""
        product_description_main = product_description_main.replace("\xa0", " ") if product_description_main else ""
        # 如果主要描述为空，则用另一种方法获取
        if not product_description_main:
            product_description_main = description_main_upper_tag.text if description_main_upper_tag else ""
            product_description_main = product_description_main.replace("\xa0", " ") if product_description_main else ""

        # 产品描述（次要）
        description_side_upper_tag = product_text_info_tag.find('h3') if product_text_info_tag else None
        description_side_tag = description_side_upper_tag.find('span') if description_side_upper_tag else None
        product_description_side = description_side_tag.text if description_side_tag else ""
        product_description_side = product_description_side.replace("\xa0", " ") if product_description_side else ""
        # 如果次要描述为空，则用另一种方法获取
        if not product_description_side:
            product_description_side = description_side_upper_tag.text if description_side_upper_tag else ""
            product_description_side = product_description_side.replace("\xa0", " ") if product_description_side else ""

        # 产品详情
        product_details_tag = product_text_info_tag.find('p') if product_text_info_tag else None
        product_details = product_details_tag.text if product_details_tag else ""
        product_details = product_details.replace("\xa0", " ") if product_details else ""

        # 填充item
        product_item["product_page_url"] = product_page_url
        product_item["first_preview_pic_url"] = first_preview_pic_url
        product_item["second_preview_pic_url"] = second_preview_pic_url
        product_item["third_preview_pic_url"] = third_preview_pic_url
        product_item["product_name"] = product_name
        product_item["product_price"] = product_price
        product_item["product_description_main"] = product_description_main
        product_item["product_description_side"] = product_description_side
        product_item["product_details"] = product_details

        self.count += 1
        # logger.info(product_item)
        yield product_item

    def close(self, spider):
        logger.info(f"共爬取{self.count}个产品")
