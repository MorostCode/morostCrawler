# -*- coding: utf-8 -*- 
# @Time: 2024/6/7 上午1:40 
# @Author: morost
# @File: taptap.py 
# @desc: https://www.taptap.cn/top/download
# scrapy crawl taptapRankList --nolog

import scrapy


# Taptap游戏item
class TaptapGameItem(scrapy.Item):
    homepage_url = scrapy.Field()  # 游戏主页链接

    game_name = scrapy.Field()  # 游戏名
    icon_url = scrapy.Field()  # 图标链接
    latest_news = scrapy.Field()  # 最新动态
    taptap_tags = scrapy.Field()  # taptap标签
    score = scrapy.Field()  # 评分

    is_editor_recommend = scrapy.Field()  # 是否编辑推荐
    highest_rank = scrapy.Field()  # 热门榜最高排名
    download_count = scrapy.Field()  # 下载量
    follow_count = scrapy.Field()  # 关注量
    game_size = scrapy.Field()  # 游戏大小
    maker = scrapy.Field()  # 厂商

    promotion_video_urls = scrapy.Field()  # 宣传片链接
    real_machine_trial_urls = scrapy.Field()  # 真机试玩链接
    pic_urls = scrapy.Field()  # 图片链接

    supplier = scrapy.Field()  # 供应商
    game_tags = scrapy.Field()  # 游戏标签
    game_intro = scrapy.Field()  # 游戏简介
    developer_words = scrapy.Field()  # 开发者的话


if __name__ == '__main__':
    pass
