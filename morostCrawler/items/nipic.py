import scrapy


# 昵图网设计师主页item
class NiPicHomePageItem(scrapy.Item):
    source_url = scrapy.Field()  # 爬取来源链接

    homepage_url = scrapy.Field()  # 设计师主页链接
    designer_name = scrapy.Field()  # 设计师名称
    avatar_pic_url = scrapy.Field()  # 头像链接

    works_list_page_url = scrapy.Field()  # 作品列表页链接
    works_num = scrapy.Field()  # 作品数量
    works_total_page_num = scrapy.Field()  # 作品总页数


# 昵图网设计师作品item
class NiPicWorksItem(scrapy.Item):
    designer_id = scrapy.Field()  # 设计师id
    works_name = scrapy.Field()  # 作品名称
    works_page_url = scrapy.Field()  # 作品详情页链接
    works_pic_url = scrapy.Field()  # 作品图片链接
    works_upload_time = scrapy.Field()  # 作品上传时间
    works_number = scrapy.Field()  # 作品编号

    # works_list_page_link = scrapy.Field()  # 作品所在列表页链接
    # works_list_page_num = scrapy.Field()  # 当前作品列表页页码
