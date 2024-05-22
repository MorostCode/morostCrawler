# from datetime import datetime
#
# from loguru import logger
#
#
# class NiPicHomePagePipeline:
#     def process_item(self, item, spider):
#         if item.__class__.__name__ != "NiPicHomePageItem":
#             return item
#         logger.info("进入NiPicHomePagePipeline，开始处理NiPicHomePageItem")
#
#         source_url = item.get("source_url", None)
#         home_page_link = item.get("home_page_link", None)
#         name = item.get("name", None)
#
#         if source_url:
#             # 更新设计师主页信息
#             nipic_user_info = (ImusaeNipicUser.select().
#                                where(ImusaeNipicUser.home_page_link == source_url).
#                                get_or_none())
#             if nipic_user_info:
#                 if home_page_link and name and source_url == home_page_link:
#                     nipic_user_info.home_page_link = home_page_link
#                     nipic_user_info.name = name
#                     nipic_user_info.total_page_num = item.get("total_page_num", nipic_user_info.total_page_num)
#                     nipic_user_info.current_page_num = 1
#                     nipic_user_info.collect_status = 1
#                     nipic_user_info.save()
#                     logger.info(f"设计师主页信息更新成功 {home_page_link}")
#                 else:
#                     nipic_user_info.collect_status = 3
#                     nipic_user_info.save()
#                     logger.warning(f"设计师主页信息更新失败 {home_page_link}")
#                     return item
#
#         return item
#
#
# class NiPicWorkPipeline:
#     def process_item(self, item, spider):
#         if item.__class__.__name__ != "NiPicWorkItem":
#             return item
#         logger.info("进入NiPicWorkPipeline，开始处理NiPicWorkItem")
#
#         home_page_link = item.get("home_page_link", None)
#         if home_page_link:
#             # 获取设计师主页信息
#             nipic_user_info = (ImusaeNipicUser.select().
#                                where(ImusaeNipicUser.home_page_link == home_page_link).
#                                get_or_none())
#             if nipic_user_info:
#                 uid = nipic_user_info.uid
#                 work_name = item.get("work_name", None)
#                 work_list_page_link = item.get("work_list_page_link", None)
#                 work_list_page_num = item.get("work_list_page_num", 1)
#                 work_page_link = item.get("work_page_link", None)
#                 work_pic_link = item.get("work_pic_link", None)
#                 work_upload_time = item.get("work_upload_time", None)
#                 work_upload_time = datetime.strptime(work_upload_time, "%Y-%m-%d") if work_upload_time else None
#                 work_number = item.get("work_number", None)
#
#                 # 判断作品所在页码是否为已爬取页码，如果不是则更新
#                 if work_list_page_num:
#                     if work_list_page_num > nipic_user_info.current_page_num:
#                         nipic_user_info.current_page_num = work_list_page_num
#                         nipic_user_info.save()
#                         logger.info(f"设计师主页 页码信息 更新成功 {home_page_link} 现在页码为 {work_list_page_num}")
#                     if work_list_page_num == nipic_user_info.total_page_num:
#                         nipic_user_info.collect_status = 2
#                         nipic_user_info.save()
#                         logger.info(f"设计师作品已爬取到最后一页 {home_page_link}")
#
#                 # 查看是否已经存在
#                 nipic_pic_info = (ImusaeNipicPic.select().
#                                   where(ImusaeNipicPic.work_page_link == work_page_link).
#                                   get_or_none())
#                 if nipic_pic_info:
#                     logger.info(f"作品信息已存在 {work_name}")
#                     return item
#
#                 # 保存作品信息
#                 nipic_pic_info = ImusaeNipicPic(
#                     uid=uid,
#                     work_name=work_name,
#                     work_list_page_link=work_list_page_link,
#                     work_list_page_num=work_list_page_num,
#                     work_page_link=work_page_link,
#                     work_pic_link=work_pic_link,
#                     work_upload_time=work_upload_time,
#                     work_number=work_number,
#                 )
#                 nipic_pic_info.save()
#                 logger.info(f"作品信息保存成功 {work_name}")
#
#         return item
