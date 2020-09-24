# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EshopgameItem(scrapy.Item):
    # define the fields for your item here like:
    game_name = scrapy.Field()
    sale_time = scrapy.Field()
    price = scrapy.Field()
    imgurl = scrapy.Field()
    supported_platforms = scrapy.Field()
    game_type = scrapy.Field()
    publisher = scrapy.Field()
    language = scrapy.Field()
    game_size = scrapy.Field()
    player_num = scrapy.Field()
    online_player_num = scrapy.Field()