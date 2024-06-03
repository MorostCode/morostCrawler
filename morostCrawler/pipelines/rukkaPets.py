# -*- coding: utf-8 -*- 
# @Time: 2024/5/30 下午1:32 
# @Author: morost
# @File: rukkaPets.py 
# @desc: https://luhta.com/global/en/c/rukka-pets/products
# scrapy crawl rukkaPets --nolog

import os.path

import requests
from loguru import logger

import pandas as pd


class RukkaPetsPipeline:
    def process_item(self, item, spider):
        if item.__class__.__name__ != "RukkaPetsProductItem":
            return item
        logger.info("进入RukkaPetsPipeline，开始处理RukkaPetsProductItem")

        # 创建字典，键是列名，值是数据
        data = {
            "产品详情页链接": [item['product_page_url']],
            "产品名称": [item['product_name']],
            "产品价格": [item['product_price']],
            "首张预览图片链接": [item['first_preview_pic_url']],
            "第二张预览图片链接": [item['second_preview_pic_url']],
            "第三张预览图片链接": [item['third_preview_pic_url']],
            "产品类型": [item['product_type']],
            "产品信息": [item['product_information']],
            "产品详情": [item['product_details']],
            "产品材料": [item['product_material']],
            "护理说明": [item['care_instructions']]
        }

        # 图片下载文件夹“E:\Github\morostCrawler\files\rukkaPetsPics”
        pics_dir = r"E:\Github\morostCrawler\files\rukkaPetsPics"
        product_name = item['product_name']
        # 下载第一张图
        if item['first_preview_pic_url']:
            first_preview_pic_url = item['first_preview_pic_url']
            print(first_preview_pic_url)
            first_preview_pic_name = f"{product_name}_1.jpg"
            first_preview_pic_path = os.path.join(pics_dir, first_preview_pic_name)
            if os.path.exists(first_preview_pic_path):
                logger.info(f"图片已存在：{first_preview_pic_path}")
            else:
                first_preview_pic_content = requests.get(first_preview_pic_url).content
                with open(first_preview_pic_path, 'wb') as f:
                    f.write(first_preview_pic_content)
                logger.info(f"图片已下载：{first_preview_pic_path}")
        # 下载第二张图
        if item['second_preview_pic_url']:
            second_preview_pic_url = item['second_preview_pic_url']
            print(second_preview_pic_url)
            second_preview_pic_name = f"{product_name}_2.jpg"
            second_preview_pic_path = os.path.join(pics_dir, second_preview_pic_name)
            if os.path.exists(second_preview_pic_path):
                logger.info(f"图片已存在：{second_preview_pic_path}")
            else:
                second_preview_pic_content = requests.get(second_preview_pic_url).content
                with open(second_preview_pic_path, 'wb') as f:
                    f.write(second_preview_pic_content)
                logger.info(f"图片已下载：{second_preview_pic_path}")
        # 下载第三张图
        if item['third_preview_pic_url']:
            third_preview_pic_url = item['third_preview_pic_url']
            print(third_preview_pic_url)
            third_preview_pic_name = f"{product_name}_3.jpg"
            third_preview_pic_path = os.path.join(pics_dir, third_preview_pic_name)
            if os.path.exists(third_preview_pic_path):
                logger.info(f"图片已存在：{third_preview_pic_path}")
            else:
                third_preview_pic_content = requests.get(third_preview_pic_url).content
                with open(third_preview_pic_path, 'wb') as f:
                    f.write(third_preview_pic_content)
                logger.info(f"图片已下载：{third_preview_pic_path}")

        # 创建一个DataFrame
        df = pd.DataFrame(data)

        # 定义文件路径
        file_path = r"E:\Github\morostCrawler\files\rukkaPets.xlsx"

        # 如果文件不存在，写入数据并添加表头
        # 如果文件存在，追加写入数据，不添加表头
        if not os.path.exists(file_path):
            logger.info("文件不存在，写入数据并添加表头")
            df.to_excel(file_path, index=False)
        else:
            logger.info("文件存在，追加写入数据，不添加表头")
            with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                # 将数据追加到已有的工作表中
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)

        return item


if __name__ == '__main__':
    import pandas as pd

    # 读取Excel文件
    file_path = r'E:\Github\morostCrawler\files\rukkaPets.xlsx'
    excel_data = pd.read_excel(file_path)

    # 将数据转换为HTML格式并嵌入图片
    html = '<html><head><title>Product Data</title></head><body>'
    html += '<table border="1" style="border-collapse:collapse;">'
    html += '<tr>'
    for column in excel_data.columns:
        html += f'<th>{column}</th>'
    html += '</tr>'

    for i, row in excel_data.iterrows():
        html += '<tr>'
        for column, cell in row.items():
            if column == "产品详情页链接":
                pass
            if column == '产品名称':
                # 获取产品详情页链接
                link = row.get('产品详情页链接', '')
                html += f'<td><a href="{link}" target="_blank">{cell}</a></td>'
            elif '图片链接' in column:
                html += f'<td><a href="{cell}" target="_blank"><img src="{cell}" alt="Image" style="max-height:300px; max-width:300px;"></a></td>'
            else:
                html += f'<td>{cell}</td>'
        html += '</tr>'

    html += '</table></body></html>'

    # 将HTML保存到文件
    output_path = r'E:\Github\morostCrawler\files\rukkaPets.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
