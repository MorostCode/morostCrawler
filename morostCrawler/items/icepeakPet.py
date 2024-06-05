# -*- coding: utf-8 -*- 
# @Time: 2024/6/3 下午11:46 
# @Author: morost
# @File: icepeakPet.py 
# @desc: https://luhta.com/global/en/c/icepeak-pet/products
# scrapy crawl icepeakPet --nolog

import scrapy


# IcepeakPet产品item
class IcepeakPetProductItem(scrapy.Item):
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
