# -*- coding: utf-8 -*- 
# @Time: 2024/5/28 下午11:33 
# @Author: morost
# @File: toyFox.py 
# @desc: https://cloakanddawggie.com/collections/all
# scrapy crawl toyFox --nolog

import scrapy


# toyFox产品item
class ToyFoxProductItem(scrapy.Item):
    product_page_url = scrapy.Field()  # 产品详情页链接
    first_preview_pic_url = scrapy.Field()  # 首张预览图片链接
    second_preview_pic_url = scrapy.Field()  # 第二张预览图片链接
    third_preview_pic_url = scrapy.Field()  # 第三张预览图片链接
    product_name = scrapy.Field()  # 产品名称
    product_price = scrapy.Field()  # 产品价格
    product_description_main = scrapy.Field()  # 产品描述（主要）
    product_description_side = scrapy.Field()  # 产品描述（次要）
    product_details = scrapy.Field()  # 产品详情
