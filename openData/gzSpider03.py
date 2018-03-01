# *-* encoding = utf-8 *-* 
# author: pengr

from spider import Spider
import json
import requests
import re
import os
import time
import queue
import threading

''' 全局变量，用来存储获取文件url的id参数与格式参数'''
data_id = []
queueLock = threading.Lock()
exitFlag = 0

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


'''多线程进行下载'''
class GzSpiderThread(threading.Thread):

    def __init__ (self,threadID,q,cookie,proxies):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q
        self.s = requests.Session()
        headers = {
            'Host':'www.gzdata.gov.cn',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.8.3.16721'
        }
        self.timeout=3
        print('---')
        #self.s.get('http://www.gzdata.gov.cn/index.html',cookies=cookie,headers =headers,proxies=self.proxies)
        self.s.get('http://www.gzdata.gov.cn/index.html',cookies=cookie,headers =headers,proxies=proxies,timeout = self.timeout)
        self.proxies =proxies
        

    def run(self):
     
        print('thread'+str(self.threadID)+'-'*10+'start')
         
        item = process_run(self.q)

        response = requests.get(self.geturl(item['id']))
        with open(item['filename'],'wb') as code:
                code.write(response.content)

        print('thread'+str(self.threadID)+'-'*10+'end')

    def geturl(self,id):
     
        time.sleep(2)
        try:
            seed_url = 'http://www.gzdata.gov.cn/dataopen/api/'
            stamp = 1512390694437
            param = "?callback=jQuery111309967397004365921_1512390694429&_="

            # id参数 1474264646836
            '''
            with open('cookie.txt','r',encoding='utf-8') as f:
                cookie=f.read()
            cookies=json.loads(cookie)
            '''

            
            url = seed_url+'filedata/'+str(id)+param+str(stamp)
            response = self.s.get(url,proxies=self.proxies,timeout=self.timeout)

            ''' 获取请求参数中的shortUrl值'''
            shorturl = parseresponse(response)['data']['shortUrl']

            url = seed_url+'url/'+shorturl+param+str(stamp+1)
            response = self.s.get(url,proxies=self.proxies,timeout=self.timeout)

            '''获取下载url'''
            realurl = parseresponse(response)['data']['realUrl']
            return realurl
        except Exception as e:
            print(e)
            return


def process_run(q):
    while not exitFlag:
        queueLock.acquire()
        if not q.empty():
            item = q.get()
            queueLock.release()
        else:
            queueLock.release()
            return
        #print(item)
        


    
'''将服务器端请求的数据规范化'''
def parseresponse(response):
    response = str(response.content,'utf-8')
    response = re.sub("/\*\*/\w+\d+\(",'',response)
    response = re.sub('\);','',response)
    return json.loads(response)

'''多个登录id多个cookies'''       
def getcookies():
    with open('cookie.txt','r',encoding='utf-8') as f:
        cookie=f.read()
    return json.loads(cookie)

def getip():
    with open('ip.txt','r',encoding='utf-8')  as f:
        ips = f.readlines()
    ip_list = []
    url = "http://ip.chinaz.com/getip.aspx"
    timeout = 3
    for proxy in ips:
        try:
            ip = proxy.strip().split("\t")
            proxy_host = "http://"+ip[0]+":"+ip[1]
            proxy_temp = {"http":proxy_host}
            res = requests.get(url,proxies = proxy_temp,timeout = timeout)
            #print(res.text)
            if re.match('\{.*?\}',res.text):
                print(proxy_temp)
                ip_list.append(proxy_temp)
            
        except :
            print(ip[0]+'--无效')
            continue

    return ip_list


'''启动多线成开始下载'''
def getdata():
    cookieList = getcookies()
  
    queueLock = threading.Lock()
    workQueue = queue.Queue(len(data_id))
    threads = []
    threadID = 1


    # 创建新线程
    for i in range(4):
        #print(cookieList[i])
        thread = GzSpiderThread(i, workQueue, cookieList[i]['cookie'], cookieList[i]['proxies'])
        thread.start()
        threads.append(thread)
    
    print('-----'*10)

    # 填充队列
    queueLock.acquire()
    for word in data_id:
        workQueue.put(word)
    queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    print ("退出主线程")

if __name__ == '__main__':
    '''贵州'''
    page = 4
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
    getdata()