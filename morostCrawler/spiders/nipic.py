import re

import scrapy
from loguru import logger
from bs4 import BeautifulSoup

from scrapy.utils.project import get_project_settings

from morostCrawler.items.nipic import NiPicHomePageItem, NiPicWorksItem
from morostCrawler.models.db_model_crawler import SpiderNipicDesigner, SpiderNipicPic


# 昵图网设计师主页爬虫-----------------------------------------------------------------------------------------------------
class NiPicHomePageSpider(scrapy.Spider):
    name = "niPicHomePage"
    allowed_domains = ["hi.nipic.com", "nipic.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取链接
        self.start_url = self.get_nipic_homepage()
        # self.start_url = "https://hi.nipic.com/people/32158254/index.html"
        logger.info(f"NiPicHomePageSpider {self.start_url}")

    def get_nipic_homepage(self):
        # 获取一个需要爬取的设计师信息
        designer_info = (SpiderNipicDesigner.select().
                         where((SpiderNipicDesigner.crawl_status == 1) | (SpiderNipicDesigner.crawl_status == 5)).
                         get_or_none())
        if designer_info and designer_info.homepage_url:
            if designer_info.homepage_url.startswith("https://hi.nipic.com/people/"):
                return designer_info.homepage_url
            else:
                # 链接格式不合法，更新为采集失败
                designer_info.crawl_status = 4
                designer_info.save()
                logger.warning(f"设计师主页链接不合法 {designer_info.home_page_link}")
                return None
        else:
            return None

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,
                             callback=self.parse,
                             headers=self.headers)

    def parse(self, response, **kwargs):
        # 创建item
        nipic_homepage_item = NiPicHomePageItem()

        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取设计师主页链接
        homepage_url = response.url

        # 获取设计师名称
        designer_name_tag = soup.find('b', attrs={"class": "fl font16 mr5 font-bold"})
        designer_name = designer_name_tag.text if designer_name_tag else ""

        # 获取头像链接
        avatar_tag = soup.find('div', attrs={"class": "fl relative mr10 hi-avatar-box"})
        avatar_pic_tag = avatar_tag.find('img') if avatar_tag else None
        avatar_pic_url = avatar_pic_tag.get('src') if avatar_pic_tag else ""

        # 获取作品列表页链接
        works_list_page_tag = soup.find('a', text="查看所有非商用作品>>")
        works_list_page_url = works_list_page_tag.get('href') if works_list_page_tag else ""
        works_list_page_url = f"https:{works_list_page_url}" if not works_list_page_url.startswith("https:") else works_list_page_url

        # 填充数据
        nipic_homepage_item['source_url'] = self.start_url
        nipic_homepage_item['homepage_url'] = homepage_url
        nipic_homepage_item['designer_name'] = designer_name
        nipic_homepage_item['avatar_pic_url'] = avatar_pic_url
        nipic_homepage_item['works_list_page_url'] = works_list_page_url

        # print(nipic_homepage_item)
        yield nipic_homepage_item


# 昵图网设计师作品爬虫-----------------------------------------------------------------------------------------------------
class NiPicWorkSpider(scrapy.Spider):
    name = "niPicWork"
    allowed_domains = ["hi.nipic.com", "nipic.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取信息
        self.start_info = self.get_designer_info()
        # self.start_info = {"designer_id": 1, "works_page_url": "https://hi.nipic.com/people/32158254/ni"}
        logger.info(f"NiPicWorkSpider {self.start_info}")

    def get_designer_info(self):
        # 获取一个需要爬取的设计师信息
        designer_info = (SpiderNipicDesigner.select().
                         where(SpiderNipicDesigner.crawl_status == 2).
                         get_or_none())
        if designer_info and designer_info.works_list_page_url:
            if designer_info.works_list_page_url.startswith("https://hi.nipic.com/people/") and \
               designer_info.works_list_page_url.endswith("ni/"):
                return {"designer_id": designer_info.id, "works_page_url": designer_info.works_list_page_url}
            else:
                # 链接格式不合法，更新为采集失败
                designer_info.crawl_status = 4
                designer_info.save()
                logger.warning(f"设计师作品页链接不合法 {designer_info.works_list_page_url}")
                return None
        else:
            return None

    def start_requests(self):
        if self.start_info:
            yield scrapy.Request(url=self.start_info["works_page_url"],
                                 callback=self.parse,
                                 headers=self.headers)

    def parse(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取作品总页数（获取不到则为1）
        last_page_tag = soup.find('a', attrs={"title": "最后页"})
        last_page_link = last_page_tag.get('href') if last_page_tag else ""
        total_page_num = re.search(r"page=(\d+)", last_page_link).group(1) if last_page_link else 1

        # 循环爬取每一个作品列表页
        for page_num in range(1, int(total_page_num) + 1):
            works_list_page_link = f"{response.url}?page={page_num}"
            yield scrapy.Request(url=works_list_page_link,
                                 callback=self.parse_works_list_page,
                                 headers=self.headers)

    def parse_works_list_page(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取作品简略信息
        works_tags = soup.find_all('div', attrs={"class": "fl person-works-item"})
        if works_tags:
            for works_tag in works_tags:
                nipic_works_item = NiPicWorksItem()
                nipic_works_item["designer_id"] = self.start_info["designer_id"]

                # 获取作品名称
                works_name_upper_tag = works_tag.find('div', attrs={"class": "person-works-name ellipsis"})
                works_name_tag = works_name_upper_tag.find('a') if works_name_upper_tag else None
                works_name = works_name_tag.text if works_name_tag else ""
                nipic_works_item['works_name'] = works_name

                # 获取作品详情页链接
                works_page_url_upper_tag = works_tag.find('div', attrs={"class": "person-works-img"})
                works_page_url_tag = works_page_url_upper_tag.find('a') if works_page_url_upper_tag else None
                works_page_url = works_page_url_tag.get('href') if works_page_url_tag else ""
                works_page_url = "https:" + works_page_url if works_page_url_tag else ""
                nipic_works_item['works_page_url'] = works_page_url

                yield scrapy.Request(url=nipic_works_item['works_page_url'],
                                     callback=self.parse_works_page,
                                     headers=self.headers,
                                     meta={"item": nipic_works_item})

    def parse_works_page(self, response, **kwargs):
        # 获取上一层级的item
        nipic_works_item = response.meta["item"]

        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取作品图片链接
        works_pic_url_tag = soup.find('img', attrs={"class": "works-img"})
        works_pic_url = works_pic_url_tag.get('src') if works_pic_url_tag else ""
        works_pic_url = "https:" + works_pic_url if works_pic_url_tag else ""
        nipic_works_item['works_pic_url'] = works_pic_url

        # 获取作品上传时间
        works_upload_time_upper_tag = soup.find('span', attrs={"itemprop": "addtime"})
        works_upload_time_tag = works_upload_time_upper_tag.find('span') if works_upload_time_upper_tag else None
        works_upload_time = works_upload_time_tag.text if works_upload_time_tag else ""
        works_upload_time = works_upload_time.replace("/", "-") if works_upload_time else ""
        nipic_works_item['works_upload_time'] = works_upload_time

        # 获取作品编号
        works_number_upper_tag = soup.find('span', attrs={"itemprop": "number"})
        works_number_tag = works_number_upper_tag.find('span') if works_number_upper_tag else None
        works_number = works_number_tag.text if works_number_tag else ""
        nipic_works_item['works_number'] = works_number

        # print(nipic_works_item)
        yield nipic_works_item

    def close(self, spider):
        # 更新记录为爬取完成
        if self.start_info:
            designer_info = SpiderNipicDesigner.get_by_id(self.start_info['designer_id'])
            if designer_info:
                # 统计作品总数
                works_num = SpiderNipicPic.select().where(SpiderNipicPic.designer_id == self.start_info['designer_id']).count()
                designer_info.works_num = works_num
                designer_info.crawl_status = 3
                designer_info.save()
                logger.info(f"设计师作品爬取完成 {designer_info.homepage_url}")
