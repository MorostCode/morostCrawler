"""
    selenium: https://selenium-python.readthedocs.io/index.html
    peewee: https://docs.peewee-orm.com/en/latest/index.html
    pyautogui: https://pyautogui.readthedocs.io/en/latest/index.html
    tween: https://github.com/asweigart/pytweening
    APScheduler: https://apscheduler.readthedocs.io/en/stable/index.html
"""
import morostCrawler.pipelines.design006

# Scrapy settings for morostCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "morostCrawler"

SPIDER_MODULES = ["morostCrawler.spiders"]
NEWSPIDER_MODULE = "morostCrawler.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "morostCrawler (+http://www.yourdomain.com)"

# Obey robots.txt rules
# 设置是否遵循网站的robots.txt规则
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 同时允许的最大并发请求（默认值：16）
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 下载器在下载同一个网站下一个页面前需要等待的时间 秒（默认值：0）
DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 设置是否启用cookie（默认值：True）
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# 设置默认请求头
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# 开启爬虫中间件，可以自定义多个，数字代表优先级，越小越优先执行
# SPIDER_MIDDLEWARES = {
#    "morostCrawler.middlewares.MorostcrawlerSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# 设置下载中间件，可以自定义多个，数字代表优先级，越小越优先执行
DOWNLOADER_MIDDLEWARES = {
    "morostCrawler.middlewares.SeleniumMiddleware": 544,
    # "morostCrawler.middlewares.MorostcrawlerDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#     "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 设置数据处理管道，可以自定义多个，数字代表优先级，越小越优先执行
ITEM_PIPELINES = {
    "morostCrawler.pipelines.design006.Design006HomePagePipeline": 500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# 数据库参数
DB_PARAMS = {
    'host': 'localhost',
    'database': 'crawler',
    'user': 'postgres',
    'password': '9527',
    'port': 5432,
    'charset': 'utf8',
}
