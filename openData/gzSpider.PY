# *-* encoding = utf-8 *-* 
# author: pengr

from spider import Spider,Writer
import json
import requests
import re
import os
import time



'''处理请求的数据'''
def func(response = None, data=None ,header=None ):
    if response:
        response = str(response.content,'utf-8')
        response = re.sub("/\*\*/\w+\d+\(",'',response)
        response = re.sub('\);','',response)
        return json.loads(response)['data']['datasetlist']

    if data:
        for item in data:
            item['description'] = re.sub('<.*?>','',item['description'])

    if header:
        myheader = {
            'name':'数据目录名称',
            'description':'数据摘要',
            'topicName':'主题名称 ',
            'orgName':'数据提供方',
            'updTime':'最后更新时间',
            'format':'数据下载格式',
            'header_sort':[
                'name','description','topicName','orgName','updTime','format'
            ]
        }
        header['myheader'] = myheader


if __name__ == '__main__':
    '''贵州  47页'''
    page = 47
    urls = []
    for pageNo in range(1,page):
        url = "http://www.gzdata.gov.cn/dataopen/api/dataset?callback=jQuery1113095454735099338_1512229270187&pageNo="+str(pageNo)+"&pageSize=10&order=1&topicId=&orgId=&name=&dataType=0&_=1512229270189"
        urls.append(url)
    
    gzSpider = Spider.Spider()
    gzSpider(urls,method = 'get', func = func)
    # filecsv = 'source/gzdata.csv'
    # Writer.writeDataCsv(gzSpider.tableHeader,gzSpider.data,filename=filecsv)

    filexlsx = 'source/gzdata.xlsx'
    Writer.writeDataExcel(gzSpider.tableHeader,gzSpider.data,filename=filexlsx)

