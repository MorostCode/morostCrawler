# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

import scrapy
from scrapy import signals
from selenium import webdriver

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

GET_HEIGHT_JS = "return document.body.scrollHeight"
SCROLL_BOTTOM_JS = "window.scrollTo(0,document.body.scrollHeight)"


class MorostcrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class MorostcrawlerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


# selenium 驱动中间件
class SeleniumMiddleware:
    def __init__(self):
        # 没有在这里设置浏览器，因为每次请求都会创建一个中间件对象，这样会导致浏览器频繁创建和销毁，影响性能
        self.driver = None

    def process_request(self, request, spider):
        # 如果请求中携带了useSelenium参数，则使用selenium
        if request.meta.get("useSelenium", False):
            # 初始化浏览器
            print("【使用 selenium 进行网页渲染】")
            self.__init_browser(proxy=request.meta.get("proxy", None))

            # 如果请求中携带了cookies，则使用cookies
            if request.cookies:
                print("【使用cookies】")
                self.__add_cookies(request.cookies, request.url)

            # 访问页面
            self.driver.get(request.url)

            # 等待页面加载
            # print(f"【等待加载：{request.meta.get('waitTime', 3)}秒】")
            time.sleep(request.meta.get("waitTime", 3))

            # 如果请求中携带了rollDown参数，则下滑页面
            if request.meta.get("rollDown", False):
                print("【开始下滑页面……】")
                self.__roll_down()
                print("【页面加载完毕】")

            # 获取页面源码
            try:
                html = self.driver.page_source
                current_url = self.driver.current_url
                self.driver.close()
                self.driver.quit()
                # 返回一个response响应对象给引擎，引擎会认为是下载器返回的响应，默认交给spider解析
                return scrapy.http.HtmlResponse(url=current_url, body=html.encode("utf-8"), encoding="utf-8", request=request)
            except Exception as e:
                self.driver.close()
                self.driver.quit()
                spider.logger.error(e)
                return None
        else:
            return None

    # 初始化浏览器
    def __init_browser(self, proxy=None):
        # 设置浏览器
        options = webdriver.EdgeOptions()
        # 设置页面加载策略：normal，eager，none
        options.page_load_strategy = 'eager'

        # 设置无界面模式并设置请求头，防止被识别为爬虫
        options.add_argument("--headless")
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
        options.add_argument("--no-sandbox")  # 无沙盒模式
        options.add_argument("--disable-extensions")  # 禁用扩展
        options.add_argument("–-disable-gpu")  # 禁用GPU加速
        options.add_argument("--log-level=3")  # 隐藏日志
        options.add_argument("--disable-notifications")  # 禁用通知
        options.add_argument("--guest")  # 访客模式，去掉同步设置窗口与个性化设置窗口
        options.add_argument('--disable-blink-features=AutomationControlled')  # 隐藏selenium特征

        # 启用开发者模式，防止被识别为爬虫
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("detach", True)  # 使浏览器在调试时不会关闭

        # 设置代理
        if proxy:
            print(f"【使用代理：{':'.join(proxy)}】")
            options.add_argument(f"--proxy-server=http://{':'.join(proxy)}")  # 隧道域名:端口号

        # 设置浏览器
        self.driver = webdriver.Edge(options=options)

        # 去除navigator.webdriver检测
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })

        # 设置页面加载超时时间（避免因为网络不稳定导致的页面已经出现但是没有加载完毕而判断超时的情况）
        self.driver.set_page_load_timeout(30)

    def __add_cookies(self, cookies, url):
        self.driver.get(url)
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def __roll_down(self):
        # 获取当前页面高度
        height = self.driver.execute_script(GET_HEIGHT_JS)
        # 下滑页面
        self.driver.execute_script(SCROLL_BOTTOM_JS)
        # 等待加载时间
        time.sleep(3)
        # 获取新的页面高度
        new_height = self.driver.execute_script(GET_HEIGHT_JS)
        # 如果新的页面高度不等于旧的页面高度，说明页面还在加载，继续下滑
        while new_height != height:
            height = new_height
            self.driver.execute_script(SCROLL_BOTTOM_JS)
            time.sleep(3)
            new_height = self.driver.execute_script(GET_HEIGHT_JS)