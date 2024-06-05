# -*- coding: utf-8 -*- 
# @Time: 2024/6/5 下午10:45 
# @Author: morost
# @File: nonStop.py 
# @desc: https://www.nonstopdogwear.com/en/for-dogs/
# scrapy crawl nonStop --nolog

import scrapy


# NonStop产品item
class NonStopProductItem(scrapy.Item):
    product_page_url = scrapy.Field()  # 产品详情页链接
    first_preview_pic_url = scrapy.Field()  # 首张预览图片链接
    second_preview_pic_url = scrapy.Field()  # 第二张预览图片链接
    third_preview_pic_url = scrapy.Field()  # 第三张预览图片链接
    product_name = scrapy.Field()  # 产品名称
    product_type = scrapy.Field()  # 产品类型
    product_price = scrapy.Field()  # 产品价格
    product_details = scrapy.Field()  # 产品详情
