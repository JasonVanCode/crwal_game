# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import pymysql
import datetime

def mysqlCon():
    return pymysql.connect("192.168.8.152","root","root","my_project")

class EshopgameImagePipeline(ImagesPipeline):
     
    def get_media_requests(self, item, info):
        # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
        # yield Request(url=item['url'],meta={'name':item['title']})
        yield scrapy.FormRequest(url=item['imgurl'])
        # pass
    
#     重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
#     接收上面meta传递过来的图片名称
# 　　我写的图片名
    def file_path(self, request, response=None, info=None):
        # name = request.meta['name']
        # 根据情况来选择,如果保存图片的名字成一个体系,那么可以使用这个
        filename  = request.url.split('/')[-1]
        return filename

    def item_completed(self, results, item, info):
        # 是一个元组，第一个元素是布尔值表示是否成功
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['true_imgurl'] = image_paths[0]
        return item

class EshopgameMysqlPipeline:
    def process_item(self, item, spider):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #连接数据库
        db = mysqlCon()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # SQL 插入语句
        sql = "INSERT INTO eshop_game(game_name, \
                sale_time, price, imgurl,true_imgurl,supported_platforms,game_type,publisher,language,game_size,player_num,online_player_num,ctime) \
                VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                (item['game_name'], item['sale_time'], item['price'], item['imgurl'],item['true_imgurl'],item['supported_platforms'],item['game_type'],item['publisher'],item['language'],item['game_size'],item['player_num'],item['online_player_num'],now_time)

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
            
        # 关闭数据库连接
        db.close()

        return item