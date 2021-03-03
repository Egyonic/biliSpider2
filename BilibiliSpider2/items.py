# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Bilibilispider2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    desc = scrapy.Field()
    pictures = scrapy.Field()


class AlbumItem(scrapy.Item):
    identity = scrapy.Field()
    desc = scrapy.Field()
    pictures = scrapy.Field()
    doc_id = scrapy.Field()
    uid = scrapy.Field()

    def __init__(self):
        super(AlbumItem, self).__init__(self)
        self['identity'] = 'AlbumItem'
