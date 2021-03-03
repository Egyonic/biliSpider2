import scrapy
from BilibiliSpider2.items import AlbumItem
import requests
import BilibiliSpider2.settings as settings
import os


class GetimageSpider(scrapy.Spider):
    name = 'getImage'
    # allowed_domains = ['www.xxx.com']
    # url to get album one page data,
    one_page_data_url = 'https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid={uid}&page_num={page}&page_size=30&biz=all'
    # url to get the count of upload
    count_data_url = 'https://api.vc.bilibili.com/link_draw/v1/doc/upload_count?uid={uid}'
    start_urls = []

    uid = 23148330  # user id to scrawl
    page_size = 30
    max_page = 0
    page_num = 0  # current page
    page_limit = 10  # page number start fom 0

    def __init__(self):
        res = requests.get(url=self.count_data_url.format(uid=self.uid))
        count = res.json()['data']['all_count']  # get count info
        self.max_page = int(count / self.page_size) + 1  # set max page to reach
        print(f'create urls ---- there are {self.max_page} pages')

        user_dir = settings.IMAGES_STORE + str(self.uid) + '/'
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        print('images will save in ' + user_dir)

        #  creat urls for every page
        # use min to limit the page number
        for index in range(min(self.max_page, self.page_limit)):
            url = self.one_page_data_url.format(uid=self.uid, page=index)
            print('have created url: ' + url)
            self.start_urls.append(url)

    def parse(self, response):
        #  return a json object including data in one page
        data_obj = response.json()
        msg = data_obj['msg']
        print(msg + ' get object count ' + str(len(data_obj['data']['items'])))
        items = data_obj['data']['items']
        for item in items:
            album_item = AlbumItem()
            album_item['desc'] = item['description']
            album_item['pictures'] = item['pictures']
            album_item['doc_id'] = item['doc_id']
            album_item['uid'] = item['poster_uid']

            yield album_item

    # 关闭浏览器
    # def close(self, spider):
    #     self.bro.quit()
