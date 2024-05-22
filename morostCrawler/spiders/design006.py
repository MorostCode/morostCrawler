import scrapy
from loguru import logger
from bs4 import BeautifulSoup

from scrapy.utils.project import get_project_settings

from morostCrawler.items.design006 import Design006HomePageItem
from morostCrawler.models.db_model_crawler import SpiderDesign006Designer


# 享设计设计师主页爬虫-----------------------------------------------------------------------------------------------------
class Design006HomePageSpider(scrapy.Spider):
    name = "design006HomePage"
    allowed_domains = ["design006.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取链接
        self.start_url = self.get_design006_homepage()
        # self.start_url = "https://www.design006.com/homepage-529868"
        logger.info(f"Design006HomePageSpider {self.start_url}")

    def get_design006_homepage(self):
        # 获取一个需要爬取的设计师信息
        designer_info = (SpiderDesign006Designer.select().
                         where((SpiderDesign006Designer.crawl_status == 1) | (SpiderDesign006Designer.crawl_status == 5)).
                         order_by(SpiderDesign006Designer.crawl_status.desc()).
                         get_or_none())
        if designer_info and designer_info.homepage_url:
            if designer_info.homepage_url.startswith("https://www.design006.com/homepage"):
                return designer_info.homepage_url
            else:
                # 链接格式不合法，更新为采集失败
                designer_info.crawl_status = 4
                designer_info.save()
                logger.warning(f"设计师主页链接不合法 {designer_info.homepage_url}")
                return None
        else:
            return None

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,
                             callback=self.parse,
                             headers=self.headers,
                             meta={"useSelenium": True,
                                   "rollDown": True})

    def parse(self, response, **kwargs):
        # 创建item
        design006_homepage_item = Design006HomePageItem()

        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取设计师主页链接
        homepage_url = response.url

        # 获取设计师名称
        avatar_tag = soup.find('div', attrs={"class": "headimg_class"})
        designer_name_space_tag = avatar_tag.find_next_sibling('div') if avatar_tag else None
        designer_name_tags = designer_name_space_tag.find_all('div') if designer_name_space_tag else []
        designer_name_tag = designer_name_tags[1] if designer_name_tags else None
        designer_name = designer_name_tag.text if designer_name_tag else ""
        # name_tagB = soup.find('font', attrs={"class": "nickname_hover"})
        # nameB = name_tagB.text if name_tagB else ""

        # 获取作品数量
        works_num_previous_tag = soup.find('div', text="作品数")
        works_num_tag = works_num_previous_tag.find_next_sibling('div') if works_num_previous_tag else None
        works_num = int(works_num_tag.text) if works_num_tag else ""

        # 获取设计师等级
        designer_level_tag = soup.find('div', attrs={"class": "name_not_curr name_curr level_curr_div"})
        designer_level = designer_level_tag.text if designer_level_tag else ""

        # 获取头像链接
        avatar_tag = soup.find('div', attrs={"class": "headimg_class"})
        avatar_pic_tag = avatar_tag.find('img') if avatar_tag else None
        avatar_pic_url = avatar_pic_tag.get('src') if avatar_pic_tag else ""

        # 获取作品信息
        works_infos = list(dict())
        works_tags = soup.find_all('li', attrs={"class": "item"})
        if works_tags:
            for works_tag in works_tags:
                works_info = dict()
                # 获取作品名称
                works_name_upper_tag = works_tag.find('div', attrs={"class": "con"})
                works_name_tag = works_name_upper_tag.find('a') if works_name_upper_tag else None
                works_name = works_name_tag.text if works_name_tag else ""
                works_info['works_name'] = works_name

                # 获取作品详情页链接
                works_page_url_tag = works_tag.find('a')
                works_page_url = works_page_url_tag.get('href') if works_page_url_tag else ""
                works_info['works_page_url'] = works_page_url

                # 获取作品图链接
                pic_prev_url_tag = works_tag.find('img')
                pic_prev_url = pic_prev_url_tag.get('src') if pic_prev_url_tag else ""
                pic_url = pic_prev_url.split("?x-oss")[0]
                works_info['works_pic_url'] = pic_url

                # 获取作品上传时间
                works_upload_time_text = pic_url.split("com/")[-1].split("/")[0] if pic_url else ""
                works_upload_time = works_upload_time_text[:4] + "-" + works_upload_time_text[4:] if works_upload_time_text else ""
                works_info['works_upload_time'] = works_upload_time

                works_infos.append(works_info)

        # 填充数据
        design006_homepage_item['source_url'] = self.start_url
        design006_homepage_item['homepage_url'] = homepage_url
        design006_homepage_item['designer_name'] = designer_name
        design006_homepage_item['works_num'] = works_num
        design006_homepage_item['designer_level'] = designer_level
        design006_homepage_item['avatar_pic_url'] = avatar_pic_url
        design006_homepage_item['works_infos'] = works_infos

        # print(design006_homepage_item)
        yield design006_homepage_item
