# *-* encoding = utf-8 *-* 
# author: pengr

from spider import Spider,Writer
import json
import requests
import re
import os
import time
import multiprocessing



'''处理请求的数据'''
def func(response = None, data=None ,header=None ):
    if response:
        return handleResponse(response.text)['datasetlist'] 

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
            'download_url':'文件url',
            'download_file':'文件',
            'calls':'调用量',
            'views': '浏览量'
            'header_sort':[
                'name','description','topicName','orgName','updTime','format','download_url','download_file','calls','views'
            ]
        }
        header['myheader'] = myheader

def handleResponse(response): 
    response = re.sub("/\*\*/\w+\d+\(",'',response)
    response = re.sub('\);','',response)
    response = re.sub("'",'"',response)
    return json.loads(response)['data']

def downloadfile(data):
    print('\t-------'+data['id'][0])
    timeout = 3
    download_url = [] 
    download_file = []
    for id in data['id']:
        url = 'http://www.gzdata.gov.cn/dataopen/api/filedata/{}?callback=jQuery1113020766250509768724_1529302845176&_=1529302845184'.format(id)
        try:
            response = requests.get(url,timeout=timeout) 
            res = handleResponse(response.text) 
            download_file.append(res['remark'])
            url = 'http://www.gzdata.gov.cn/dataopen/api/url/{}?callback=jQuery1113006382656167261302_1529303313503&_=1529303313512'.format(res['shortUrl'])
            try:
                response = requests.get(url)
                download_url.append(handleResponse(response.text)['realUrl'])
               
            except Exception as e:
                raise e
        except Exception as e:
            print(e)

        dir = os.getcwd()+'/source/gz/'+data['name']
        if not os.path.exists(dir):
            os.mkdir(dir)

        data['download_url'] = ' '.join(download_url)
        for url,file in zip(download_url,download_file):
            res = requests.get(url)
            with open(dir+'/'+file,'wb+') as f:
                f.write(res.content)


if __name__ == '__main__':
    '''贵州  全部161页 文件61页'''
    page = 161
    urls = []
    for pageNo in range(1,page):  
        ''' dataType= (空)全部， dataType=0 文件，dataType=1 接口，dataType=3 应用 '''
        url = "http://www.gzdata.gov.cn/dataopen/api/dataset?callback=jQuery1113095454735099338_1512229270187&pageNo="+str(pageNo)+"&pageSize=10&order=0&topicId=&orgId=&name=&dataType=0&_=1512229270189"
        urls.append(url)
    
    gzSpider = Spider.Spider()
    gzSpider(urls,method = 'get', func = func)

    path = os.getcwd()
    dir = path+'/source/gz'
    if not os.path.exists(dir):
        os.mkdir(dir)

    print('\n'.join(['-'*40,'\t下载全部资源','-'*40]))

    pool = multiprocessing.Pool(processes = 6)
    pool.map(downloadfile, gzSpider.data)
    pool.close() # 关闭进程池，表示不能在往进程池中添加进程
    pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用

    # downloadfile(gzSpider.data[0])


    # filecsv = 'source/gzdata.csv'
    # Writer.writeDataCsv(gzSpider.tableHeader,gzSpider.data,filename=filecsv)

    # filexlsx = 'source/gzdata.xlsx'
    Writer.writeDataExcel(gzSpider.tableHeader,gzSpider.data,filename=filexlsx)
    # Writer.writeDataMongo(gzSpider.tableHeader,gzSpider.data,collection_name='db.gz_catalog')
    print('\tend!') 



    # http://gzopen.oss-cn-guizhou-a.aliyuncs.com/%E8%B4%B5%E5%B7%9E%E7%9C%81%E6%8A%95%E8%B5%84%E4%BF%83%E8%BF%9B%E5%B1%802015%E5%B9%B4%E5%BA%A6%E9%83%A8%E9%97%A8%E5%86%B3%E7%AE%97%E5%8F%8A%E2%80%9C%E4%B8%89%E5%85%AC%E2%80%9D%E7%BB%8F%E8%B4%B9%E5%86%B3%E7%AE%97%E4%BF%A1%E6%81%AF%E5%85%AC%E5%BC%80%E8%A1%A8.xls?Expires=1809321363&OSSAccessKeyId=cRMkEl0MLhpV9l7g&Signature=3SfWDvwyUL8f9F6LpcIwcpkSwzU%3D
