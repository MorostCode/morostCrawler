# -*- coding: utf-8 -*- 
# @Time: 2024/6/5 下午10:44 
# @Author: morost
# @File: nonStop.py 
# @desc: https://www.nonstopdogwear.com/en/for-dogs/
# scrapy crawl nonStop --nolog

import os

import requests
import pandas as pd
from loguru import logger


class NonStopPipeline:
    def process_item(self, item, spider):
        if item.__class__.__name__ != "NonStopProductItem":
            return item
        logger.info("进入NonStopPipeline，开始处理NonStopProductItem")


if __name__ == '__main__':
    pass
