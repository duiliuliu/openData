# *-* encoding = utf-8 *-* 
# author: pengr

import requests
from spider import JsonParse
import multiprocessing

class Spider(object):
    def __init__(self,func=None):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
        }
        '''
            表格的头部，可通过对获取的数据集合获取，也可通过func函数自定义
        '''
        self.tableHeader =  {}
        self.tableHeader_self = {}  #自定义表头
        self.data = []
        self.clean_func = func  #数据处理

    '''
    urls 需要访问的url集合，method 请求方式， data 请求中传入的数据， file 数据保存文件， func 对数据处理的中间函数
    保留函数，对旧有模块的支持
    '''
    def __call__(self, urls, func, headers = None, method = 'get', data = None, file = None,  ):
        if headers:
            self.headers =headers
        try:
            i = 0
            for url in urls:
                if method == 'post':
                    response = requests.post(url,headers = self.headers, data=data)
                else :
                    response = requests.get(url,headers = self.headers)

                response = func(response = response)

 
                for item in response:
                    self._parseData(item)
                
                i+=1
                print('-------'+str(i))
                
            func(data = self.data,header=self.tableHeader)    
                    
        except Exception as e:
            raise e 

    #爬取数据
    def crawl(self, url, headers = None, method = 'get', data = None):
        if headers:
            self.headers =headers

        if method == 'post':
            response = requests.post(url,headers = self.headers, data=data)
        else :
            response = requests.get(url,headers = self.headers)

        if self.clean_func:
            response = self.clean_func(response = response)
        else:
            response = response.json()

        for item in response:
            self._parseData(item)

    #多进程爬取数据
    def mul_crawl(self):
        pool = multiprocessing.Pool(processes = 4)
        pool.apply_async(self.crawl, ('url', ))
        pool.close() # 关闭进程池，表示不能在往进程池中添加进程
        pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用

    #设置自定义表头
    def set_tableHeader_self(self,tableHeader_self):
        self.tableHeader_self = tableHeader_self

    #设置清理数据函数
    def set_func(self,func):
        self.clean_func = func

    #将数据写入Excel表中 , all==true时表示有自定义头部的话，将自定义头部与所有数据头部都写入
    def write_excel(self, all=False):
        pass

    #将数据写入Csv表中
    def write_csv(self, all=False):
        pass

    #将数据处理
    def data_clean(self):
        self.clean_func(data=self.data, header=self.tableHeader)  

    #对获取的数据解析
    def _parseData(self,content):
        parse = JsonParse.JsonParse()
        parse.parse(content)
        self.data.append(parse.getItems())
        self.tableHeader.update(parse.getHeaders())

    #通过索引获取列
    def getcolumn_by_index(self,index):
        pass

    #通过列明获取列
    def getcolumn_by_name(self,name):
        pass

    
     
if __name__ == '__main__':
    pass

    

