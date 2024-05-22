import scrapy


# 抖音用户主页item
class DouYinHomePageItem(scrapy.Item):
    uid = scrapy.Field()  # 抖音号唯一识别码
    account_name = scrapy.Field()  # 抖音号名
    home_page = scrapy.Field()  # 抖音主页链接
    head_img = scrapy.Field()  # 抖音头像链接
    video_page_links = scrapy.Field()  # 视频主页链接列表


# 抖音视频主页item
class DouYinVideoItem(scrapy.Item):
    video_page_link = scrapy.Field()  # 视频主页链接
    video_download_link = scrapy.Field()  # 视频下载链接
    video_title = scrapy.Field()  # 视频标题
    video_duration = scrapy.Field()  # 视频时长
    release_time = scrapy.Field()  # 视频发布时间
