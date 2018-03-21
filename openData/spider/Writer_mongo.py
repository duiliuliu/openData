# *-* coding : utf-8 *-*
# author : pengr

import pymongo

'''
    目录数据存储 db.catalog
    资源数据 暂定
'''


def writeDataMongo(headers,items):

    conn = pymongo.MongoClient()        #连接本地服务器，pymongo.Connection('10.32.38.50',27017)
    #选择opendata库
    db = conn.opendata

    #建立索引 暂时选择抓取到的数据id做索引
    db.catalog.ensure_index('cata_id',unique=True)

    try:
        db.catalog.insert_one(headers)
    except :
        print('header已存在')

    try:
        db.catalog.insert_many(items,ordered=False)    #,codec_options={'ordered':False}
    except Exception as e:
        print(e)

    print('数据插入成功')

   





