# *-* encoding = utf-8 *-* 
# author: pengr

import xlsxwriter
import csv
import pymongo

'''
    将数据写入Excel中
    header  Excel表头
    items   数据项
    filename    文件名称
'''
def writeDataExcel(header,items,filename = 'cachedata.xlsx'):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    h_format = workbook.add_format()
    h_format.set_bold()
    h_format.set_bg_color('#90EE90')

    if 'myheader' in header:
        #自定义的头部
        myheader = header['myheader']
        myheader2 = []

        for info in myheader['header_sort']:
            if not header[info]:
                worksheet.write(row,col,myheader[info],h_format)
                myheader2.append(info)
                col += 1
            else:
                worksheet.merge_range(row,col,row,col+len(header[info])-1,info,h_format)
                for sub in header[info]:
                    worksheet.write(row+1,col,sub,h_format)
                    myheader2.append(sub)
                    col += 1
        row += 1
        header = myheader2
    
    else:
        myheader = []
        #数据项头部
        for info in header:
            if not header[info] :
                worksheet.write(row,col,info,h_format)
                myheader.append(info)
                col += 1
            else:
                worksheet.merge_range (row,col,row,col+len(header[info])-1,info,h_format)
                for sub in header[info]:
                    worksheet.write(row+1,col,sub,h_format)
                    myheader.append(sub)
                    col += 1
        row += 1
        header = myheader

    
    for item in items:
        row += 1
        col = 0
        for key in header:
            if key in item:
                worksheet.write(row,col,str(item[key]))
            col+=1

    workbook.close()


'''
    将数据写入csv中
    header  csv表头
    items   数据项
    filename 文件名称
'''
def writeDataCsv(header,items,filename = 'cachedata.csv'):
    with open(filename,'a+',encoding='utf8') as file:
        f_csv = csv.DictWriter(file, header)
        f_csv.writeheader()
        f_csv.writerows(items)



'''
    目录数据存储 db.catalog
    资源数据 暂定
    headers 数据头部
    items  数据集合
    collection_name 集合名
    index 索引
'''
def writeDataMongo(headers, items, collection_name, index='cata_id'):

    conn = pymongo.MongoClient()        #连接本地服务器，pymongo.Connection('10.32.38.50',27017)
    #选择opendata库
    db = conn.opendata

    #建立索引 暂时选择抓取到的数据id做索引
    db.catalog.ensure_index(index,unique=True)

    collection = eval(collection_name)

    try:
        collection.insert_one(headers)
    except :
        print('header已存在')

    try:
        collection.insert_many(items,ordered=False)    #
    except Exception as e:
        print(e)

    print('数据插入成功')
            
