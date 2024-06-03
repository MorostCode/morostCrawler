# -*- coding: utf-8 -*- 
# @Time: 2024/5/29 下午8:44 
# @Author: morost
# @File: rukkaPets.py 
# @desc: https://luhta.com/global/en/c/rukka-pets/products
# scrapy crawl rukkaPets --nolog

import scrapy


# RukkaPets产品item
class RukkaPetsProductItem(scrapy.Item):
    product_page_url = scrapy.Field()  # 产品详情页链接
    first_preview_pic_url = scrapy.Field()  # 首张预览图片链接
    second_preview_pic_url = scrapy.Field()  # 第二张预览图片链接
    third_preview_pic_url = scrapy.Field()  # 第三张预览图片链接
    product_name = scrapy.Field()  # 产品名称
    product_type = scrapy.Field()  # 产品类型
    product_price = scrapy.Field()  # 产品价格
    product_information = scrapy.Field()  # 产品信息
    product_details = scrapy.Field()  # 产品详情
    product_material = scrapy.Field()  # 产品材料
    care_instructions = scrapy.Field()  # 护理说明
