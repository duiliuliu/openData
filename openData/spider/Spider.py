# *-* encoding = utf-8 *-* 
# author: pengr

import requests
from spider import JsonParse


class Spider(object):
    def __init__(self,):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
        }
        '''
            表格的头部，可通过对获取的数据集合获取，也可通过func函数自定义
        '''
        self.tableHeader =  {}
        self.data = []
        self.file= []

    '''
    urls 需要访问的url集合，method 请求方式， data 请求中传入的数据， file 数据保存文件， func 对数据处理的中间函数
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
                    print('-------'+str(i))
                    response = requests.get(url,headers = self.headers)

                response = func(response = response)

 
                for item in response:
                    self.parseData(item)
                
                i+=1
                print('-------'+str(i))
                
            func(data = self.data,header=self.tableHeader)    
                    
        except Exception as e:
            raise e 
        
    def parseData(self,content):
        parse = JsonParse.JsonParse()
        parse.parse(content)
        self.data.append(parse.getItems())
        self.tableHeader.update(parse.getHeaders())

    
     
if __name__ == '__main__':
    pass

    

  
    

