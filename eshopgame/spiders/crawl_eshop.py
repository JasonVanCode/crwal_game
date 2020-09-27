import scrapy
from eshopgame.items import EshopgameItem

class CrawlEshopSpider(scrapy.Spider):

    name = 'crawl_eshop'

    allowed_domains = ['store.nintendo.com.hk']

    start_urls = ['http://store.nintendo.com.hk/']

    def parse(self, response):
        for val in response.xpath('//div[@class="category-product-list"]/div[@class="category-product-item"]'):
            data = EshopgameItem()
            #下面是获取该节点下面所有的字符串，包括子节点下面的字符串
            # sale_date = val.xpath('.//div[2]/div[1]/div[1]')[0]
            # data['sale_date'] = sale_date.xpath('string(.)').extract_first()
            data['price'] = val.xpath('.//div[2]/div[1]/div[2]/div[1]/span[1]/span[1]/span[1]/text()').extract_first()
            data['imgurl'] = val.xpath('.//div[1]/a/span/span/img/@data-src').extract_first()
            detail_info = val.xpath('.//div[1]/a/@href').extract_first()
            if detail_info:
                resquest =  scrapy.Request(url=detail_info,callback=self.parse_detailinfo)
                resquest.meta['item'] = data
                yield resquest
            else:
                yield data
          


    def parse_detailinfo(self,response):

        data = response.meta['item']
        maincontent = response.xpath('//*[@id="maincontent"]')
        #它会取得所有class为a的元素
        data['game_name'] = maincontent.xpath('./div[2]/div/div[1]/div[1]/div[2]/h1/span/text()').extract_first()
        data['sale_time'] = maincontent.xpath('./div[2]/div/div[1]/div[1]/div[6]/div[1]/div[1]/div[3]/div[2]/text()').extract_first()
        data['game_type'] = maincontent.xpath('./div[2]/div/div[1]/div[1]/div[6]/div[1]/div[1]/div[2]/div[2]/text()').extract_first()
        data['supported_platforms'] = maincontent.xpath('./div[2]/div/div[1]/div[1]/div[6]/div[1]/div[1]/div[1]/div[2]/text()').extract_first()
        data['publisher'] = maincontent.xpath('./div[2]/div/div[1]/div[1]/div[6]/div[1]/div[1]/div[4]/div[2]/text()').extract_first()
        data['language'] = maincontent.xpath('./div[2]/div/div[1]/div[1]/div[6]/div[1]/div[2]/div[1]/div[2]/text()').extract_first()
        data['game_size'] = maincontent.xpath('./div[2]/div/div[1]/div[1]/div[6]/div[1]/div[2]/div[2]/div[2]/text()').extract_first()
        data['player_num'] = maincontent.xpath('./div[2]/div/div[1]/div[1]/div[6]/div[1]/div[1]/div[5]/div[2]/text()').extract_first()
        data['online_player_num'] = maincontent.xpath('./div[2]/div/div[1]/div[1]/div[6]/div[1]/div[2]/div[3]/div[2]/text()').extract_first()

        yield data