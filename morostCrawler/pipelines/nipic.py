from datetime import datetime

from loguru import logger

from morostCrawler.models.db_model_crawler import SpiderNipicDesigner, SpiderNipicPic


class NiPicHomePagePipeline:
    def process_item(self, item, spider):
        if item.__class__.__name__ != "NiPicHomePageItem":
            return item
        logger.info("进入NiPicHomePagePipeline，开始处理NiPicHomePageItem")

        source_url = item.get("source_url", None)
        homepage_url = item.get("homepage_url", None)
        designer_name = item.get("designer_name", None)

        if source_url:
            # 获取设计师信息
            designer_info = (SpiderNipicDesigner.select().
                             where(SpiderNipicDesigner.homepage_url == source_url).
                             get_or_none())
            if designer_info:
                if designer_name and source_url == homepage_url:
                    designer_info.homepage_url = homepage_url
                    designer_info.designer_name = designer_name
                    designer_info.avatar_pic_url = item.get("avatar_pic_url", designer_info.avatar_pic_url)
                    designer_info.works_list_page_url = item.get("works_list_page_url", designer_info.works_list_page_url)
                    designer_info.crawl_status = 2
                    designer_info.save()
                    logger.info(f"设计师主页信息更新成功 {homepage_url}")
                else:
                    designer_info.crawl_status = 4
                    designer_info.save()
                    logger.warning(f"设计师主页信息更新失败 {homepage_url}")
                    return item

        return item


class NiPicWorksPipeline:
    def process_item(self, item, spider):
        if item.__class__.__name__ != "NiPicWorksItem":
            return item
        logger.info("进入NiPicWorksPipeline，开始处理NiPicWorksItem")

        designer_id = item.get("designer_id", None)

        if designer_id:
            # 获取设计师主页信息
            designer_info = SpiderNipicDesigner.get_by_id(designer_id)
            if designer_info:
                works_name = item.get("work_name", None)
                works_page_url = item.get("works_page_url", None)
                works_pic_url = item.get("works_pic_url", None)
                works_upload_time = item.get("work_upload_time", None)
                works_upload_time = datetime.strptime(works_upload_time, "%Y-%m-%d") if works_upload_time else None
                works_number = item.get("works_number", None)

                # 查看是否已经存在
                pic_exist = (SpiderNipicPic.select().
                             where(SpiderNipicPic.works_page_url == works_page_url).
                             get_or_none())
                if pic_exist:
                    logger.info(f"作品信息已存在 {works_name}")
                    return item

                # 保存作品信息
                pic_info = SpiderNipicPic(
                    works_name=works_name,
                    works_page_url=works_page_url,
                    works_pic_url=works_pic_url,
                    works_upload_time=works_upload_time,
                    works_number=works_number,
                )
                pic_info.save()
                logger.info(f"作品信息保存成功 {works_name}")

        return item
