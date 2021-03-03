# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import scrapy
import requests
from scrapy.http import HtmlResponse
from time import sleep


class Bilibilispider2DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.


    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # t_url = request.url
        # see if the url is the specific url
        if request.url.startswith('https://api.vc.bilibili.com/link_draw/v1/doc/doc_list'):
            # print('----------- request middlewares processing ------------')
            headers = {
                'Host': 'api.vc.bilibili.com',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
                'Origin': 'https://space.bilibili.com',
                'Referer': 'https://space.bilibili.com/1975826/album',
                'cookies': "l=v; _uuid=3F201C0A-2A35-BB9C-CD10-A3BA67792FF431208infoc; buvid3=0C5E1447-AF8B-41EB-8AB7-B50DE1AD7E4370378infoc; PVID=1; sid=m5mkk98n; CURRENT_FNVAL=80; rpdid=|(u)~m~llR~Y0J'ulmRRJYk|m; bp_video_offset_8583228=477746396499671921; bp_t_offset_8583228=477902106249238060; fingerprint=7189169a9159e87320a1df6b914a6b5d; buvid_fp=0C5E1447-AF8B-41EB-8AB7-B50DE1AD7E4370378infoc; buvid_fp_plain=0C5E1447-AF8B-41EB-8AB7-B50DE1AD7E4370378infoc; DedeUserID=8583228; DedeUserID__ckMd5=046ffac17ddebb99; SESSDATA=9b7b3aa6%2C1625624661%2Cde95f*11; bili_jct=a9e85726a80634d152b43813086d954b; blackside_state=1; LIVE_BUVID=AUTO4516100910828931"
            }

            # send a reqest by requests
            res = requests.get(url=request.url, headers=headers)

            new_response = HtmlResponse(url=request.url, body=res.text,
                                         encoding='utf-8', request=request)

            return new_response

        return None
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass
