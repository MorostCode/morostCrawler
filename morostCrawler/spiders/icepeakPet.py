# -*- coding: utf-8 -*- 
# @Time: 2024/6/3 下午11:41 
# @Author: morost
# @File: icepeakPet.py 
# @desc: https://luhta.com/fi/fi/c/icepeak-pet/tuotteet
# scrapy crawl icepeakPet --nolog

import re
import math
import scrapy
from loguru import logger
from bs4 import BeautifulSoup

from scrapy.utils.project import get_project_settings

from morostCrawler.items.icepeakPet import IcepeakPetProductItem


# IcepeakPet 产品爬虫-----------------------------------------------------------------------------------------------------
class IcepeakPetSpider(scrapy.Spider):
    name = "icepeakPet"
    allowed_domains = ["luhta.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取链接
        self.start_url = "https://luhta.com/fi/fi/c/icepeak-pet/tuotteet"
        # 产品计数
        self.count = 0
        # 产品总数
        self.product_total_num = 0
        logger.info(f"IcepeakPetSpider {self.start_url}")

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,
                             callback=self.parse,
                             headers=self.headers)

    # 解析产品主页
    def parse(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取页面上显示的产品总数
        product_total_num_tag = soup.find('span', attrs={"class": "product-list-toolbar__count"})
        product_total_num_string = product_total_num_tag.text if product_total_num_tag else ""
        self.product_total_num = int(product_total_num_string.split(" ")[0]) if product_total_num_string else 0

        # 获取页码区域标签
        pagination_tag = soup.find('p', attrs={"class": "progress-text text--center"})
        pagination_text = pagination_tag.text if pagination_tag else ""
        # 使用正则表达式提取指定内容
        page_product_num = int(re.search(r"Viewed (\d+) of (\d+) products", pagination_text).group(1)) if pagination_text else 0
        all_product_num = int(re.search(r"Viewed (\d+) of (\d+) products", pagination_text).group(2)) if pagination_text else 0
        # 计算总页码
        page_num = math.ceil(all_product_num / page_product_num) if page_product_num else 1

        # 直接访问最后一页
        page_url = f"{self.start_url}?currentPage={page_num}"
        yield scrapy.Request(url=page_url,
                             callback=self.parse_product_list_page,
                             headers=self.headers)

    # 解析产品列表页
    def parse_product_list_page(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取产品列表区域标签
        product_list_tag = soup.find('div', attrs={"class": "product-list"})

        if product_list_tag:
            # 获取所有产品详情页链接tag
            product_info_link_tags = product_list_tag.find_all('a', attrs={"class": "product-info-link"})

            # 循环爬取每一个产品详情页链接
            for product_info_link_tag in product_info_link_tags:
                # 获取产品详情页链接
                product_page_url = product_info_link_tag.get('href') if product_info_link_tag else ""
                product_page_url = f"https://luhta.com{product_page_url}" if not product_page_url.startswith("https://luhta.com") else product_page_url

                print(product_page_url)

                # 请求产品详情页
                yield scrapy.Request(url=product_page_url,
                                     callback=self.parse_product_page,
                                     headers=self.headers)

    # 解析产品详情页
    def parse_product_page(self, response, **kwargs):
        # 新建产品item
        product_item = IcepeakPetProductItem()

        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 产品详情页链接
        product_page_url = response.url

        # 获取class为product-image-gallery__thumbnails no-scrollbar的div标签
        product_image_gallery_tag = soup.find('div', attrs={"class": "product-image-gallery__thumbnails no-scrollbar"})
        # 获取下面所有type为button的button标签
        product_image_button_tags = product_image_gallery_tag.find_all('button', attrs={"type": "button"})

        # 首张预览图片链接
        first_preview_pic_url = ""
        if len(product_image_button_tags) >= 1:
            first_preview_pic_tag = product_image_button_tags[0].find('img')
            first_preview_pic_url = first_preview_pic_tag.get('src') if first_preview_pic_tag else ""
            first_preview_pic_url = first_preview_pic_url.split("?quality")[0]

        # 第二张预览图片链接
        second_preview_pic_url = ""
        if len(product_image_button_tags) >= 2:
            second_preview_pic_tag = product_image_button_tags[1].find('img')
            second_preview_pic_url = second_preview_pic_tag.get('src') if second_preview_pic_tag else ""
            second_preview_pic_url = second_preview_pic_url.split("?quality")[0]

        # 第三张预览图片链接
        third_preview_pic_url = ""
        if len(product_image_button_tags) >= 3:
            third_preview_pic_tag = product_image_button_tags[2].find('img')
            third_preview_pic_url = third_preview_pic_tag.get('src') if third_preview_pic_tag else ""
            third_preview_pic_url = third_preview_pic_url.split("?quality")[0]

        product_header_tag = soup.find('header', attrs={"class": "product__header"})
        # 产品名称
        product_name_tag = product_header_tag.find('h1') if product_header_tag else None
        product_name = product_name_tag.text if product_name_tag else ""
        product_name = product_name.replace("\n", "").strip()
        # 产品类型
        product_type_tag = product_header_tag.find('h2') if product_header_tag else None
        product_type = product_type_tag.text if product_type_tag else ""
        product_type = product_type.replace("\n", "").strip()

        # 产品价格
        product_price_tag = soup.find('p', attrs={"class": "normal-price"})
        product_price = product_price_tag.text if product_price_tag else ""

        # 下拉菜单信息
        product_information = ""
        product_details = ""
        product_material = ""
        care_instructions = ""
        product_information_button_tags = soup.find_all('button', attrs={"class": "product-accordion-item__title"})
        for product_information_button_tag in product_information_button_tags:
            # 获取button标签的文本
            button_text = product_information_button_tag.text.strip()
            # 根据按钮文字判断标签类型
            if button_text == "Product information":  # 产品信息
                product_information_upper_tag = product_information_button_tag.find_next('div', attrs={"class": "product-accordion-item__content-inner"})
                product_information_tag = product_information_upper_tag.find('div', attrs={"class": "product-details"})
                product_information = " ".join([p_tag.text.strip().replace("\n", "") for p_tag in product_information_tag.find_all('p')]) if product_information_tag else ""
            elif button_text == "Details":  # 产品详情
                product_details_upper_tag = product_information_button_tag.find_next('div', attrs={"class": "product-accordion-item__content-inner"})
                product_details_tag = product_details_upper_tag.find('li', attrs={"class": "feature-list-item"})
                product_details = " ".join([p_tag.text.strip().replace("\n", "") for p_tag in product_details_tag.find_all('span')]) if product_details_tag else ""
            elif button_text == "Material":  # 产品材料
                product_material_upper_tag = product_information_button_tag.find_next('div', attrs={"class": "product-accordion-item__content-inner"})
                product_material_tag = product_material_upper_tag.find('ul', attrs={"class": "feature-list"})
                product_material = " ".join([p_tag.text.strip().replace("\n", "") for p_tag in product_material_tag.find_all('li')]) if product_material_tag else ""
            elif button_text == "Care instructions":  # 护理说明
                care_instructions_upper_tag = product_information_button_tag.find_next('div', attrs={"class": "product-accordion-item__content-inner"})
                care_instructions_tag = care_instructions_upper_tag.find('ul', attrs={"class": "feature-list"})
                care_instructions = " ".join([p_tag.text.strip().replace("\n", "") for p_tag in care_instructions_tag.find_all('li')]) if care_instructions_tag else ""

        # 填充item
        product_item["product_page_url"] = product_page_url
        product_item['first_preview_pic_url'] = first_preview_pic_url
        product_item['second_preview_pic_url'] = second_preview_pic_url
        product_item['third_preview_pic_url'] = third_preview_pic_url
        product_item['product_name'] = product_name
        product_item['product_type'] = product_type
        product_item['product_price'] = product_price
        product_item['product_information'] = product_information
        product_item['product_details'] = product_details
        product_item['product_material'] = product_material
        product_item['care_instructions'] = care_instructions

        self.count += 1
        # logger.info(product_item)
        yield product_item

    def close(self, spider):
        logger.info(f"共爬取{self.count}个产品")
