# *-* encoding = utf-8 *-* 
# author: pengr

from spider import Spider
import json
import requests
import re
import os
import time

data_id = []

'''cookie'''
cookies = ''

'''读取cookies'''
def getcookie():
    with open('cookie00.txt','r',encoding='utf-8') as f:
        cookie=f.read()
    global cookies
    cookies = json.loads(cookie)

'''处理请求的数据'''
def func(response = None, data=None ,header=None ):
    if response:
        response = str(response.content,'utf-8')
        response = re.sub("/\*\*/\w+\d+\(",'',response)
        response = re.sub('\);','',response)
        return json.loads(response)['data']['datasetlist']

    if data: 
        for item in data:
            global data_id
            data_id.append({
                'name':item['name'],
                'id':item['id'],
                'format':item['format']
            })
            item['description'] = re.sub('<.*?>','',item['description'])
        data.insert (0,{
            'description':'数据摘要',
            'topicName':'主题名称 ',
            'orgName':'数据提供方',
            'updTime':'最后更新时间',
            'list':'数据下载'
        })


'''下载文件'''
def getdata(data_id):
    path = './source/gzdata'
    if not os.path.exists(path):
        os.makedirs('./source/gzdata')
    for item in data_id:
        '''建立子文件夹'''
        mydir = './source/gzdata/'+item['name']
        if not os.path.exists(mydir):
            os.makedirs(mydir)
        
        for i in range(1,len(item['id'])):
            myid = item['id'][i]
            form = item['format']
            print(myid)
            print(form)
            if not type(form)== list:
                filename = mydir +'/'+ str(myid)+'.'+form
            else:
                filename = mydir +'/'+ str(myid)+'.'+form[i-1]


            response = requests.get(geturl(myid))
            with open(filename,'wb') as code:
                    code.write(response.content)
        
        
'''对于不同的文件格式，需要有不同的文件写入方式'''

'''获取文件url'''
def geturl(id):
    try:
        seed_url = 'http://www.gzdata.gov.cn/dataopen/api/'
        stamp = 1512390694437
        param = "?callback=jQuery111309967397004365921_1512390694429&_="

        # id参数 1474264646836

        global cookies
        
        header={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.6.2.15784"
        }
        url = seed_url+'filedata/'+str(id)+param+str(stamp)
        response = requests.get(url,cookies=cookies,headers = header)

        ''' 获取请求参数中的shortUrl值'''
        shorturl = parseresponse(response)['data']['shortUrl']

        url = seed_url+'url/'+shorturl+param+str(stamp+1)
        response = requests.get(url,cookies=cookies,headers = header)

        '''获取下载url'''
        realurl = parseresponse(response)['data']['realUrl']
        return realurl
    except Exception as e:
        print(e)
        print('wait-----一分钟')
        time.sleep(1)
        cookies = getcookie()


def parseresponse(response):
    response = str(response.content,'utf-8')
    response = re.sub("/\*\*/\w+\d+\(",'',response)
    response = re.sub('\);','',response)
    return json.loads(response)

    

if __name__ == '__main__':
    '''贵州'''
    page = 2
    urls = []
    for pageNo in range(1,page):
        url = "http://www.gzdata.gov.cn/dataopen/api/dataset?callback=jQuery1113095454735099338_1512229270187&pageNo="+str(pageNo)+"&pageSize=10&order=1&topicId=&orgId=&name=&dataType=0&_=1512229270189"
        urls.append(url)
    
    gzSpider = Spider.Spider()
    gzSpider(urls,method = 'get', func = func)
    # filecsv = 'source/gzdata.csv'
    # filexlsx = 'source/gzdata.xlsx'
    # Spider.writeDataCsv(gzSpider.tableHeader,gzSpider.data,filename=filecsv)
    # Spider.writeDataExcel(gzSpider.tableHeader,gzSpider.data,filename=filexlsx)
    
    '''
    下载文件函数，一个账号在一段时间内可以下载一定数量的文件，然后需要等待一定的时间。
    如果登入多个账号，自动登录需要解决验证码。 
    '''
    getdata(data_id)
