import scrapy
from loguru import logger
from bs4 import BeautifulSoup

from scrapy.utils.project import get_project_settings

from morostCrawler.items.douyin import DouYinHomePageItem, DouYinVideoItem


# 抖音用户主页爬虫--------------------------------------------------------------------------------------------------------
class DouyinHomePageSpider(scrapy.Spider):
    name = "douyinHomePage"
    allowed_domains = ["www.douyin.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取链接
        # self.start_url = self.get_douyin_homepage()
        self.start_url = ["https://www.douyin.com/user/MS4wLjABAAAAsASbPTIyspRgEKVXWQhA4cgVvfYsipEjeg-Sda1HJXXm79LWMyNO5pzgCFDwX4MD"]
        logger.info(f"DouyinHomePageSpider {self.start_url}")

    # # 从数据库中获取未爬取的抖音主页
    # def get_douyin_homepage(self):
    #     # 获取一个没有爬取完成的抖音主页链接
    #     douyin_account_info = (DistributeDouyinAccount.select().
    #                            where(DistributeDouyinAccount.status == 0).
    #                            get_or_none())
    #     if douyin_account_info:
    #         if douyin_account_info.home_page and douyin_account_info.home_page.startswith("https://www.douyin.com/user/"):
    #             return douyin_account_info.home_page
    #         else:
    #             # 链接格式不合法，更新为采集失败
    #             douyin_account_info.status = 3
    #             douyin_account_info.save()
    #             logger.warning(f"链接格式不合法 {douyin_account_info.home_page}")
    #             return None
    #     else:
    #         return None

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,
                             callback=self.parse,
                             headers=self.headers,
                             meta={"useSelenium": True})

    def parse(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取主页下的视频链接
        video_page_links = []
        div_tag = soup.find('div', attrs={'data-e2e': 'user-post-list'})
        if div_tag:
            ul_tag = div_tag.find('ul', attrs={'data-e2e': 'scroll-list'})
            if ul_tag:
                li_tags = ul_tag.find_all('li')
                if li_tags:
                    for li_tag in li_tags:
                        div_tag = li_tag.find('div')
                        if div_tag:
                            a_tag = div_tag.find('a')
                            if a_tag:
                                # 获取a标签的href
                                href = a_tag.get('href')
                                if href:
                                    if not href.startswith('/video'):  # 如果不是视频链接则跳过
                                        continue
                                    # 将href添加到爬取列表中
                                    if not href.startswith('https:'):
                                        href = 'https://www.douyin.com' + href
                                        video_page_links.append(href)

        # 获取uid
        uid_element = soup.find('span', attrs={'class': 'TVGQz3SI'})
        if uid_element:
            uid_string = uid_element.text
            uid = uid_string.split('抖音号：')[-1]
        else:
            uid = ""

        # 获取账号名
        account_name_element = soup.find('span', attrs={'class': 'j5WZzJdp'})
        account_name = account_name_element.text if account_name_element else ""

        # 获取头像链接
        head_img_div = soup.find('div', attrs={'data-e2e': 'live-avatar'})
        head_img = head_img_div.find('img').get('src') if head_img_div else ""
        if not head_img.startswith('https:'):
            head_img = 'https:' + head_img

        # 创建item，填充数据，返回
        douyin_homePage_item = DouYinHomePageItem()
        douyin_homePage_item['uid'] = uid
        douyin_homePage_item['account_name'] = account_name
        douyin_homePage_item['home_page'] = response.url
        douyin_homePage_item['head_img'] = head_img
        douyin_homePage_item['video_page_links'] = video_page_links

        print(douyin_homePage_item)
        # yield douyin_homePage_item


# 抖音视频详情页爬虫------------------------------------------------------------------------------------------------------
class DouyinVideoSpider(scrapy.Spider):
    name = "douyinVideo"
    allowed_domains = ["www.douyin.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取请求头
        self.headers = get_project_settings().getdict("DEFAULT_REQUEST_HEADERS")
        # 初始化爬取链接
        self.start_urls = self.get_douyin_video_pages()
        self.start_urls = ["https://www.douyin.com/video/7291892761215782171"]
        # logger.info(f"DouyinVideoSpider {self.start_urls}")

    # def get_douyin_video_pages(self):
    #     douyin_video_list = list()
    #     # 获取一个正在采集中的抖音账号
    #     douyin_account_info = (DistributeDouyinAccount.select().
    #                            where(DistributeDouyinAccount.status == 1).
    #                            get_or_none())
    #     if douyin_account_info:
    #         print(douyin_account_info)
    #         uid = douyin_account_info.uid
    #         # 获取该uid下所有未采集的视频记录
    #         videos = (DistributeDouyinVideo.select().
    #                   where(DistributeDouyinVideo.author_uid == uid).
    #                   where(DistributeDouyinVideo.status == 0))
    #         if videos:
    #             for video in videos:
    #                 douyin_video_list.append(video.video_page_link)
    #
    #     return douyin_video_list

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 headers=self.headers,
                                 meta={"useSelenium": True,
                                       "waitTime": 3})

    def parse(self, response, **kwargs):
        # 解析response
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取视频下载地址
        video_download_link = ""
        container_tag = soup.find('xg-video-container', attrs={'class': 'xg-video-container'})
        if container_tag:
            video_tag = container_tag.find('video')
            if video_tag:
                for source_tag in video_tag.find_all('source'):
                    video_download_link = source_tag.get('src')
                    if video_download_link:
                        if not video_download_link.startswith('https:'):
                            video_download_link = 'https:' + video_download_link

        # 获取视频标题
        video_title_element = soup.find('span', attrs={'class': 'j5WZzJdp'})
        video_title = video_title_element.text if video_title_element else ""

        # 获取视频时长
        video_duration_element = soup.find('span', attrs={'class': 'time-duration'})
        video_duration = video_duration_element.text if video_duration_element else ""

        # 获取发布时间
        release_time_element = soup.find('span', text=lambda x: x and "发布时间" in x)
        release_time = release_time_element.text.split('：')[-1] if release_time_element else ""

        # 创建item，填充数据，返回
        douyin_video_item = DouYinVideoItem()
        douyin_video_item['video_page_link'] = response.url
        douyin_video_item['video_download_link'] = video_download_link
        douyin_video_item['video_title'] = video_title
        douyin_video_item['video_duration'] = video_duration
        douyin_video_item['release_time'] = release_time

        print(douyin_video_item)
        # yield douyin_video_item
