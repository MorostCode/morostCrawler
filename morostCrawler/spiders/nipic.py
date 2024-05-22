import re
import scrapy
from loguru import logger
from bs4 import BeautifulSoup

from scrapy.utils.project import get_project_settings

from morostCrawler.items.nipic import NiPicHomePageItem, NiPicWorkItem


# 昵图网设计师主页爬虫-----------------------------------------------------------------------------------------------------
class NiPicHomePageSpider(scrapy.Spider):
    name = "niPicHomePage"
    allowed_domains = ["hi.nipic.com", "nipic.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取链接
        # self.start_url = self.get_nipic_homepage()
        self.start_url = "https://hi.nipic.com/people/32158254/ni"
        logger.info(f"NiPicHomePageSpider {self.start_url}")

    # def get_nipic_homepage(self):
    #     # 获取一个没有爬取完成的设计师主页链接
    #     nipic_user_info = (ImusaeNipicUser.select().
    #                        where(ImusaeNipicUser.collect_status == 0).
    #                        get_or_none())
    #     if nipic_user_info:
    #         if nipic_user_info.home_page_link and nipic_user_info.home_page_link.startswith("https://hi.nipic.com/people/"):
    #             # 如果链接是用户主页，更新为作品列表页
    #             if nipic_user_info.home_page_link.endswith("index.html"):
    #                 nipic_user_info.home_page_link = nipic_user_info.home_page_link.replace("index.html", "ni")
    #                 nipic_user_info.save()
    #             return nipic_user_info.home_page_link
    #         else:
    #             # 链接格式不合法，更新为采集失败
    #             nipic_user_info.collect_status = 3
    #             nipic_user_info.save()
    #             logger.warning(f"链接格式不合法 {nipic_user_info.home_page_link}")
    #             return None
    #     else:
    #         return None

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,
                             callback=self.parse,
                             headers=self.headers)

    def parse(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 创建item
        nipic_homepage_item = NiPicHomePageItem()

        # 获取设计师主页链接
        home_page_link = response.url
        # 获取设计师名称
        name_tag = soup.find('b', attrs={"class": "fl font16 mr5 font-bold"})
        name = name_tag.text if name_tag else ""
        # 获取作品总页数
        last_page_tag = soup.find('a', attrs={"title": "最后页"})
        last_page_link = last_page_tag.get('href') if last_page_tag else ""
        total_page_num = re.search(r"page=(\d+)", last_page_link).group(1) if last_page_link else 1

        nipic_homepage_item['source_url'] = self.start_url
        nipic_homepage_item['home_page_link'] = home_page_link
        nipic_homepage_item['name'] = name
        nipic_homepage_item['total_page_num'] = total_page_num

        print(nipic_homepage_item)
        # yield nipic_homepage_item


# 昵图网设计师作品爬虫-----------------------------------------------------------------------------------------------------
class NiPicWorkSpider(scrapy.Spider):
    name = "niPicWork"
    allowed_domains = ["hi.nipic.com", "nipic.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取链接
        # self.start_urls = self.get_nipic_work_list_pages()
        # self.start_urls = ["https://hi.nipic.com/people/32158254/ni?page=1", "https://hi.nipic.com/people/32158254/ni?page=2"]
        self.start_urls = ["https://hi.nipic.com/people/32158254/ni?page=1"]
        logger.info(f"NiPicWorkSpider {self.start_urls}")

    # def get_nipic_work_list_pages(self):
    #     work_list_pages = list()
    #     # 获取一个作品没有爬取完成的设计师下的所有未爬取的作品列表页链接
    #     nipic_user_info = (ImusaeNipicUser.select().
    #                        where(ImusaeNipicUser.collect_status == 1).
    #                        get_or_none())
    #     if nipic_user_info:
    #         for i in range(1, int(nipic_user_info.total_page_num) + 1):
    #             work_list_page_link = f"{nipic_user_info.home_page_link}?page={i}"
    #             work_list_pages.append(work_list_page_link)
    #         return work_list_pages
    #     return None

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url,
                                 callback=self.parse,
                                 headers=self.headers)

    def parse(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取设计师主页链接
        home_page_link = response.url.split("?")[0]
        # 当前作品列表页页码
        work_list_page_num_tag = soup.find('span', attrs={"class": "page-num-on"})
        work_list_page_num = int(work_list_page_num_tag.text) if work_list_page_num_tag else 1

        # 获取作品信息
        work_infos = list(dict())
        work_tags = soup.find_all('div', attrs={"class": "fl person-works-item"})
        if work_tags:
            for work_tag in work_tags:
                work_info = dict()
                # 获取作品名称
                work_name_upper_tag = work_tag.find('div', attrs={"class": "person-works-name ellipsis"})
                work_name_tag = work_name_upper_tag.find('a') if work_name_upper_tag else None
                work_name = work_name_tag.text if work_name_tag else ""
                work_info['work_name'] = work_name
                # 获取作品详情页链接
                work_page_link_upper_tag = work_tag.find('div', attrs={"class": "person-works-img"})
                work_page_link_tag = work_page_link_upper_tag.find('a') if work_page_link_upper_tag else None
                work_page_link = work_page_link_tag.get('href') if work_page_link_tag else ""
                work_page_link = "https:" + work_page_link if work_page_link_tag else ""
                work_info['work_page_link'] = work_page_link
                # 添加到作品信息列表
                work_infos.append(work_info)

        if work_infos:
            for work_info in work_infos:
                nipic_work_item = NiPicWorkItem()
                nipic_work_item['home_page_link'] = home_page_link
                nipic_work_item['work_name'] = work_info['work_name']
                nipic_work_item['work_list_page_link'] = response.url
                nipic_work_item['work_list_page_num'] = work_list_page_num
                nipic_work_item['work_page_link'] = work_info['work_page_link']

                yield scrapy.Request(url=work_info['work_page_link'],
                                     callback=self.parse_detail,
                                     headers=self.headers,
                                     meta={"item": nipic_work_item})
        else:
            nipic_work_item = NiPicWorkItem()
            nipic_work_item['home_page_link'] = home_page_link
            nipic_work_item['work_list_page_link'] = response.url
            nipic_work_item['work_list_page_num'] = work_list_page_num
            print(nipic_work_item)
            # yield nipic_work_item

    def parse_detail(self, response, **kwargs):
        # 获取上一层级的item
        item = response.meta["item"]

        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取作品图片链接
        work_pic_link_tag = soup.find('img', attrs={"class": "works-img"})
        work_pic_link = work_pic_link_tag.get('src') if work_pic_link_tag else ""
        work_pic_link = "https:" + work_pic_link if work_pic_link_tag else ""
        item['work_pic_link'] = work_pic_link

        # 获取作品上传时间
        work_upload_time_upper_tag = soup.find('span', attrs={"itemprop": "addtime"})
        work_upload_time_tag = work_upload_time_upper_tag.find('span') if work_upload_time_upper_tag else None
        work_upload_time = work_upload_time_tag.text if work_upload_time_tag else ""
        work_upload_time = work_upload_time.replace("/", "-") if work_upload_time else ""
        item['work_upload_time'] = work_upload_time

        # 获取作品编号
        work_number_upper_tag = soup.find('span', attrs={"itemprop": "number"})
        work_number_tag = work_number_upper_tag.find('span') if work_number_upper_tag else None
        work_number = work_number_tag.text if work_number_tag else ""
        item['work_number'] = work_number

        print(item)
        # yield item
