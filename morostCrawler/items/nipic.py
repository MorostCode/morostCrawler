import scrapy


# 昵图网设计师主页item
class NiPicHomePageItem(scrapy.Item):
    source_url = scrapy.Field()  # 爬取来源链接

    home_page_link = scrapy.Field()  # 设计师主页链接
    name = scrapy.Field()  # 设计师名称
    total_page_num = scrapy.Field()  # 作品总页数


# 昵图网设计师作品item
class NiPicWorkItem(scrapy.Item):
    home_page_link = scrapy.Field()  # 设计师主页链接

    work_name = scrapy.Field()  # 作品名称
    work_list_page_link = scrapy.Field()  # 作品列表页链接
    work_list_page_num = scrapy.Field()  # 当前作品列表页页码
    work_page_link = scrapy.Field()  # 作品详情页链接
    work_pic_link = scrapy.Field()  # 作品图片链接
    work_upload_time = scrapy.Field()  # 作品上传时间
    work_number = scrapy.Field()  # 作品编号
