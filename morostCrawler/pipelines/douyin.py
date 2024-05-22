# from loguru import logger
#
#
# class DouyinHomePagePipeline:
#     def process_item(self, item, spider):
#         if item.__class__.__name__ != "DouYinHomePageItem":
#             return item
#         logger.info("进入DouyinHomePagePipeline，开始处理DouYinHomePageItem")
#
#         uid = item.get('uid', None)
#         home_page = item.get('home_page', None)
#         video_page_links = item.get('video_page_links', None)
#
#         if uid and home_page:
#             account_info = (DistributeDouyinAccount.select().
#                             where(DistributeDouyinAccount.home_page == home_page).
#                             get_or_none())
#             if account_info:
#                 if account_info.uid == uid:
#                     account_info.account_name = item.get('account_name', account_info.account_name)
#                     account_info.head_img = item.get('head_img', account_info.head_img)
#                     account_info.collected_videos = len(item.get('video_page_links', []))
#                     account_info.collect_degree = 1
#                     account_info.status = 1
#                     account_info.deal_status = 0
#                     account_info.save()
#                     logger.info(f"抖音账号信息更新成功 {home_page}")
#                 else:
#                     account_info.status = 3
#                     account_info.save()
#                     logger.warning(f"抖音账号信息更新失败 {home_page}")
#                     return item
#
#             if video_page_links:
#                 for video_page_link in item.get('video_page_links'):
#                     douyin_video_info = DistributeDouyinVideo(
#                         video_page_link=video_page_link,
#                         author_uid=uid,
#                         author_name=item.get('account_name', ''),
#                         author_link=home_page,
#                         priority=1,
#                         status=0,
#                         deal_status=0,
#                         remark=""
#                     )
#                     douyin_video_info.save()
#             logger.info("DouYinHomePageItem处理完毕")
#
#         return item
#
#
# class DouyinVideoPipeline:
#     def process_item(self, item, spider):
#         if item.__class__.__name__ != "DouYinVideoItem":
#             return item
#
#         logger.info("进入DouyinVideoPipeline，开始处理DouYinVideoItem")
#
#         # # 更新distribute_douyin_video表中的记录信息
#         # # 首先确认item中的video_page_link和video_download_link不为空
#         # if item.get('video_page_link', None) and item.get('video_download_link', None):
#         #     update_query = ("UPDATE distribute_douyin_video "
#         #                     "SET video_download_link = %s, video_title = %s, video_duration = %s, release_time = %s, "
#         #                     "status = %s, deal_status = %s, remark = %s "
#         #                     "WHERE video_page_link = %s;")
#         #     self.cursor.execute(update_query, (item.get('video_download_link'),
#         #                                        item.get('video_title', ''),
#         #                                        item.get('video_duration', ''),
#         #                                        item.get('release_time', ''),
#         #                                        1, 0, "",
#         #                                        item.get('video_page_link')))
#         #     self.conn.commit()
#         #
#         #     # 根据video_page_link获取该视频的author_uid
#         #     query = "SELECT author_uid FROM distribute_douyin_video WHERE video_page_link = %s;"
#         #     self.cursor.execute(query, item.get('video_page_link'))
#         #     author_uid = self.cursor.fetchone()[0]
#         #     # 获取该author_uid的所有status为0的视频记录
#         #     query = "SELECT COUNT(*) FROM distribute_douyin_video WHERE author_uid = %s AND status = 0;"
#         #     self.cursor.execute(query, author_uid)
#         #     video_num = self.cursor.fetchone()[0]
#         #     # 如果video_num为0，则更新distribute_douyin_account表中的status为2
#         #     if video_num == 0:
#         #         update_query = "UPDATE distribute_douyin_account SET status = 2 WHERE uid = %s;"
#         #         self.cursor.execute(update_query, author_uid)
#         #         self.conn.commit()
#         #
#         # logger.info("DouYinVideoItem处理完毕")
#         return item
