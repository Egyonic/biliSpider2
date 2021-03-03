# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import requests
import os
import scrapy
from . import settings


class Bilibilispider2Pipeline:
    img_path = '/home/egyonic/Work/Python/spider/BilibiliSpider2/save/images/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
    }

    def process_item(self, item, spider):
        print(item['doc_id'])
        dir_path = self.img_path + str(item['doc_id'])
        # 1. create the directory
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        # 2. download and save the images
        if item['pictures'] is not None:
            print('download images ----------')
            for pic in item['pictures']:
                res = requests.get(pic['img_src'], headers=self.headers)
                pic_name = dir_path + '/' + pic['img_src'].split('/')[-1]
                with open(pic_name, 'wb') as fp:
                    fp.write(res.content)

        if item['desc'] is not None:
            # print(item['desc'])
            f_name = dir_path + '/' + str(item['doc_id']) + '.txt'
            with open(f_name, 'w', encoding='utf-8') as fp:
                fp.write(item['desc'])
            print('------------')

        # return item


# download images
class ImgsPipeLine(ImagesPipeline):

    # 根据图片地址进行图片数据请求
    def get_media_requests(self, item, io):
        # only for AlbumItem
        if item['identity'] == 'AlbumItem':
            print('resolve doc_id ' + str(item['doc_id']))
            dir_name = os.path.join(settings.IMAGES_STORE, str(item['uid']), str(item['doc_id']))
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            print('create sub directory: ' + dir_name)

            with open(dir_name + '/' + str(item['doc_id'])+'.txt', 'w', encoding='utf-8') as fp:
                fp.write(item['desc'])

            for pic in item['pictures']:
                # print(pic['img_src'])
                yield scrapy.Request(pic['img_src'])

    def file_path(self, request, response=None, info=None, *, item=None):
        # imgName = request.url.split('/')[-1]
        imgName = (request.url.split('/')[-1]).split('.')[0] + '.jpg'
        img_path = os.path.join(str(item['uid']), str(item['doc_id']), imgName)
        print('save file: ' + img_path)
        return img_path

    def item_completed(self, results, item, info):
        return item  # 返回给下一个即将被执行的管道类
