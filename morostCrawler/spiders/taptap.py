# -*- coding: utf-8 -*- 
# @Time: 2024/6/7 上午1:39 
# @Author: morost
# @File: taptap.py 
# @desc: https://www.taptap.cn/top/download
# scrapy crawl taptapRankList --nolog

import re

import scrapy
from loguru import logger
from bs4 import BeautifulSoup

from scrapy.utils.project import get_project_settings

from morostCrawler.items.taptap import TaptapGameItem
from morostCrawler.utils.commonFunction import strFormat


# taptap排行榜游戏爬虫----------------------------------------------------------------------------------------------------
class TaptapRankListSpider(scrapy.Spider):
    name = "taptapRankList"
    allowed_domains = ["taptap.cn"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        self.count = 0
        # 初始化爬取链接
        self.start_url = "https://www.taptap.cn/top/download"
        logger.info(f"TaptapRankListSpider {self.start_url}")

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,
                             callback=self.parse,
                             headers=self.headers,
                             meta={"useSelenium": True,
                                   "rollDown": True})

    def parse(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取class为list-content的div标签
        rank_list_div = soup.find('div', attrs={"class": "list-content"})
        # 获取rank_list_div下所有class为list-item的div标签
        game_item_divs = rank_list_div.find_all('div', attrs={"class": "list-item"}) if rank_list_div else []

        for game_item_div in game_item_divs[:5]:
            # 获取game_item_div下的a标签
            game_a_tag = game_item_div.find('a')
            # 获取a标签的href属性
            game_homepage_url = game_a_tag.get("href") if game_a_tag else None
            game_homepage_url = "https://www.taptap.cn" + game_homepage_url if game_homepage_url and not game_homepage_url.startswith("https://") else game_homepage_url

            yield scrapy.Request(url=game_homepage_url,
                                 callback=self.parse_game_homepage,
                                 headers=self.headers)

    def parse_game_homepage(self, response, **kwargs):
        # 新建item
        game_item = TaptapGameItem()

        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取游戏主要信息
        # 获取class为app-info-board的div标签
        app_info_board_div = soup.find('div', attrs={"class": "app-info-board"})

        # 获取app_info_board_div下的h1标签
        game_name_tag = app_info_board_div.find("h1") if app_info_board_div else None
        game_name = strFormat(game_name_tag.text) if game_name_tag else None

        # 获取app_info_board_div下class为tap-image的img标签
        icon_img_tag = app_info_board_div.find('img', attrs={"class": "tap-image"}) if app_info_board_div else None
        icon_url = icon_img_tag.get("src") if icon_img_tag else None

        # 获取class为tap-text tap-text__one-line caption-m12-w12 gray-08 game-desc-hints的div标签
        latest_news_tag = app_info_board_div.find('div', attrs={"class": "tap-text tap-text__one-line caption-m12-w12 gray-08 game-desc-hints"}) if app_info_board_div else None
        latest_news = strFormat(latest_news_tag.text) if latest_news_tag else None

        # 获取class为scrollable flex-center--y clickable的div标签
        taptap_tags_div = app_info_board_div.find('div', attrs={"class": "scrollable flex-center--y clickable"}) if app_info_board_div else None
        # 获取div下所有标签的文字
        taptap_tags = [strFormat(tag.text) for tag in taptap_tags_div.children if strFormat(tag.text) != ''] if taptap_tags_div else []
        taptap_tags_strig = "·".join(taptap_tags)

        # 获取class为rate-number-font app-info-board__rating font-bold的span标签
        score_tag = app_info_board_div.find('span', attrs={"class": "rate-number-font app-info-board__rating font-bold"}) if app_info_board_div else None
        score = float(strFormat(score_tag.text)) if score_tag else None

        # 获取游戏次要信息

        # 游戏多媒体信息

        # 获取游戏详细信息

        # 填充数据
        game_item['homepage_url'] = response.url
        game_item['game_name'] = game_name
        game_item['icon_url'] = icon_url
        game_item['latest_news'] = latest_news
        game_item['taptap_tags'] = taptap_tags_strig
        game_item['score'] = score

        self.count += 1
        logger.info(game_item)
        # yield game_item

    def close(self, spider):
        logger.info(f"共爬取{self.count}个游戏")


if __name__ == '__main__':
    pass
