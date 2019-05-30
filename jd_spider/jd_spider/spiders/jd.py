# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib.parse import urljoin
from jd_spider.items import JdSpiderItem
from scrapy_redis.spiders import RedisSpider


class JdSpider(RedisSpider):
    name = 'jd'
    reids_keys = 'jd:start_urls'
    allowed_domains = ['jd.com']
    # start_urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&page=1']
    # lpush jd:start_urls https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&page=1
    crawl_urls = 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&page={}'
    base_comment_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv{}&productId={}&score={}&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    base_url='https://'

    def start_requests(self):
        urls=[self.crawl_urls.format(i) for i in range(6,10)]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        print(response.url)
        contents = response.xpath('//ul[@class="gl-warp clearfix"]/li[@class="gl-item"]')
        for content in contents:
            href=content.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a/@href').extract_first()
            href =urljoin(self.base_url,href)
            # shop = content.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-shop"]//text()').extract()
            # shop = ''.join(shop).replace('\n', '').replace('\t', '')
            yield scrapy.Request(url=href,callback=self.parse_info)

    def parse_info(self,response):
        html=response.text
        commentVersion=re.search(r'commentVersion:\'(\d+)\'',html,re.S).group(1)
        productID=re.search(r'item\.jd\.com/(\d+)\.html',html,re.S).group(1)
        if commentVersion !=0:
            for score in range(1,3):
                comment_url=self.base_comment_url.format(commentVersion,productID,score)
                yield scrapy.Request(url=comment_url,callback=self.parse_comment)

    def parse_comment(self,response):
        item=JdSpiderItem()
        # html=response.text
        # if html:
        try:
            json_data=re.search(r'\((.*)\)',response.text ).group(1)
            json_data = json.loads(json_data)
            page=json_data['maxPage']
            comments=json_data['comments']
            for comment in comments:
                item['id']=comment['id']
                item['content']=comment['content'].replace('\n',',')
                item['nickname']=comment['nickname']
                item['score'] = ((response.url).split('&')[-6]).split('=')[-1]
                yield item

            current_page=((response.url).split('&')[-4]).split('=')[-1]
            if int(current_page)<page:
                next_page=(response.url).replace('page='+str(current_page),'page='+str(int(current_page)+1))
                # print('正在爬取第{}页'.format(i))
                yield scrapy.Request(url=next_page,callback=self.parse_comment)
        except:
            # print("暂无评论")
            pass



