import scrapy


# 享设计设计师主页item
class Design006HomePageItem(scrapy.Item):
    source_url = scrapy.Field()  # 爬取来源链接

    homepage_url = scrapy.Field()  # 设计师主页链接
    designer_name = scrapy.Field()  # 设计师名称
    works_num = scrapy.Field()  # 作品数量
    designer_level = scrapy.Field()  # 设计师等级
    avatar_pic_url = scrapy.Field()  # 头像链接

    """
    works_infos：
        works_name 作品名称
        works_page_url 作品详情页链接
        works_pic_url 作品图片链接
        works_upload_time 作品上传时间
    """
    works_infos = scrapy.Field()  # 作品信息列表
