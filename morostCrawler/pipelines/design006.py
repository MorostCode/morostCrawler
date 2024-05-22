from datetime import datetime

from loguru import logger

from morostCrawler.models.db_model_crawler import SpiderDesign006Designer, SpiderDesign006Pic


class Design006HomePagePipeline:
    def process_item(self, item, spider):
        if item.__class__.__name__ != "Design006HomePageItem":
            return item
        logger.info("进入Design006HomePagePipeline，开始处理Design006HomePageItem")

        source_url = item.get("source_url", None)
        homepage_url = item.get("homepage_url", None)
        designer_name = item.get("designer_name", None)

        if source_url:
            # 获取设计师信息
            designer_info = (SpiderDesign006Designer.select().
                             where(SpiderDesign006Designer.homepage_url == source_url).
                             get_or_none())
            if designer_info:
                # 更新设计师主页信息
                if designer_name and source_url == homepage_url:
                    designer_info.homepage_url = homepage_url
                    designer_info.designer_name = designer_name
                    designer_info.works_num = item.get("works_num", designer_info.works_num)
                    designer_info.designer_level = item.get("designer_level", designer_info.designer_level)
                    designer_info.avatar_pic_url = item.get("avatar_img", designer_info.avatar_pic_url)
                    designer_info.crawl_status = 2
                    designer_info.save()
                    logger.info(f"设计师主页信息更新成功 {homepage_url}")
                else:
                    designer_info.crawl_status = 4
                    designer_info.save()
                    logger.warning(f"设计师主页信息更新失败 {homepage_url}")
                    return item

                # 处理设计师作品信息
                works_infos = item.get("works_infos", [])
                exist = 0
                for works_info in works_infos:
                    works_name = works_info.get("works_name", None)
                    works_page_url = works_info.get("works_page_url", None)
                    works_pic_url = works_info.get("works_pic_url", None)
                    works_upload_time = works_info.get("works_upload_time", None)
                    works_upload_time = datetime.strptime(works_upload_time, "%Y-%m") if works_upload_time else None

                    # 查看是否已经存在
                    pic_info = (SpiderDesign006Pic.select().
                                where(SpiderDesign006Pic.works_page_url == works_page_url).
                                get_or_none())
                    if pic_info:
                        exist += 1
                        continue
                    # 保存作品信息
                    pic_info = SpiderDesign006Pic(
                        designer_id=designer_info.id,
                        works_name=works_name,
                        works_pic_url=works_pic_url,
                        works_page_url=works_page_url,
                        works_upload_time=works_upload_time,
                    )
                    pic_info.save()

                designer_info.crawl_status = 3
                designer_info.save()
                logger.info(f"设计师作品信息更新成功 {homepage_url}，{len(works_infos) - exist}个成功 {exist}个已存在")

        return item
