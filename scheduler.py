# -*- coding: utf-8 -*- 
# @Time: 2024/5/20 上午12:07 
# @Author: morost
# @File: scheduler.py 
# @desc:

import os
import time
import platform
import subprocess

from apscheduler.schedulers.background import BackgroundScheduler

sys = platform.system()


# 抖音------------------------------------------------------------------------------------------------------------------
# 用户主页爬虫
def run_douyin_home_page():
    bash = "scrapy crawl douyinHomePage --nolog"
    subprocess.run(bash, shell=True)


# 视频页爬虫
def run_douyin_video_spider():
    bash = "scrapy crawl douyinVideo --nolog"
    subprocess.run(bash, shell=True)


# 阿里1688--------------------------------------------------------------------------------------------------------------
# 公司详情页爬虫
def run_ali1688_company_detail():
    bash = "scrapy crawl ali1688CompanyDetail --nolog"
    subprocess.run(bash, shell=True)


# 产品详情页爬虫
def run_ali1688_product_detail():
    bash = "scrapy crawl ali1688ProductDetail --nolog"
    subprocess.run(bash, shell=True)


# 享设计-----------------------------------------------------------------------------------------------------------------
def run_design006_homepage():
    bash = "scrapy crawl design006HomePage --nolog"
    subprocess.run(bash, shell=True)


# 昵图网-----------------------------------------------------------------------------------------------------------------
def run_nipic_homepage():
    bash = "scrapy crawl niPicHomePage --nolog"
    subprocess.run(bash, shell=True)


def run_nipic_work():
    bash = "scrapy crawl niPicWork --nolog"
    subprocess.run(bash, shell=True)


# 保护程序
def protect():
    # 杀掉所有msedge与msedgedrive进程
    os.system('taskkill /IM msedge.exe /F')
    os.system('taskkill /IM msedgedrive.exe /F')


if __name__ == '__main__':
    scheduler = BackgroundScheduler()

    # 抖音爬虫
    # scheduler.add_job(func=run_douyin_home_page, trigger='interval', seconds=600, max_instances=1)
    # scheduler.add_job(func=run_douyin_video_spider, trigger='interval', seconds=600, max_instances=1)

    # 阿里1688爬虫
    # scheduler.add_job(func=run_ali1688_company_detail, trigger='interval', seconds=90, max_instances=1, coalesce=True)
    # scheduler.add_job(func=run_ali1688_product_detail, trigger='interval', seconds=90, max_instances=1, coalesce=True)

    # 享设计爬虫
    scheduler.add_job(func=run_design006_homepage, trigger='interval', seconds=600, max_instances=1)
    # 昵图网爬虫
    scheduler.add_job(func=run_nipic_homepage, trigger='interval', seconds=600, max_instances=1)
    scheduler.add_job(func=run_nipic_work, trigger='interval', seconds=601, max_instances=1)

    # 启动调度器
    scheduler.start()

    # 保持主线程运行
    try:
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
