# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EshopgameImagePipeline:
    def process_item(self, item, spider):
        print(item['imgurl'])
        return item

class EshopgameMysqlPipeline:
    def process_item(self, item, spider):
        print(3333333333)
        return item