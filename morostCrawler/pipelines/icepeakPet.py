# -*- coding: utf-8 -*- 
# @Time: 2024/6/3 下午11:44 
# @Author: morost
# @File: icepeakPet.py
# @desc: https://luhta.com/fi/fi/c/icepeak-pet/tuotteet
# scrapy crawl icepeakPet --nolog

import os.path

import requests
from loguru import logger


class IcepeakPetPipeline:
    def process_item(self, item, spider):
        if item.__class__.__name__ != "IcepeakPetProductItem":
            return item
        logger.info("进入IcepeakPetPipeline，开始处理IcepeakPetProductItem")


if __name__ == '__main__':
    pass
