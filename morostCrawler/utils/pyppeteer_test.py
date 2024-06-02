# -*- coding: utf-8 -*- 
# @Time: 2024/5/31 上午1:12 
# @Author: morost
# @File: pyppeteer_test.py 
# @desc: pyppeteer_test

import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth


async def main():
    # 使用launch方法创建一个浏览器对象（打开浏览器）
    # 关闭无头模式设置headless=False（默认是True）
    # 设置args参数来关闭“Chrome 正受到自动测试软件的控制”提示
    # 设置userDataDir参数来指定用户数据目录（会新建一个存储用户行为数据的userdata文件夹）
    # await等待浏览器启动完毕
    browser = await launch(headless=False,
                           args=['--disable-infobars'],
                           userDataDir='./userdata')

    # 使用newPage方法创建了一个Page对象（打开新标签页）
    # await等待标签页创建完毕
    page = await browser.newPage()

    # 隐藏特征
    await stealth(page)

    # 使用goto方法打开目标网址
    await page.goto('https://top.baidu.com/board?tab=realtime')

    # 调用Page对象下的evaluate方法可以执行JS语句
    dimensions = await page.evaluate('''() => {
               return {
                   width: document.documentElement.clientWidth,
                   height: document.documentElement.clientHeight,
                   deviceScaleFactor: window.devicePixelRatio,
               }
           }''')
    print(dimensions)

    # 获取页面内容
    page_text = await page.content()
    print(page_text)

    await asyncio.sleep(3)

    # 使用close方法关闭浏览器
    await browser.close()

if __name__ == '__main__':
    # 创建一个事件循环
    asyncio.get_event_loop().run_until_complete(main())
