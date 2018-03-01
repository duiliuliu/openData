# *-* encoding = utf-8 *-* 
# author: pengr

import requests
import csv
from spider import JsonParse
import xlsxwriter

class Spider(object):
    def __init__(self,):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
        }
        self.tableHeader = {
            'level':0,  #层级为0
            'header':set()  #表头集合
        }
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
        '''
        需要更新
        '''
        self.tableHeader.update(parse.getKeys())

        
def writeDataExcel(header,items,filename = 'cachedata.xlsx'):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    h_format = workbook.add_format()
    h_format.set_bold()
    h_format.set_bg_color('green')

    for info in header:
        worksheet.write(row,col,info,h_format)
        col += 1
    
    for item in items:
        row += 1
        col = 0
        for key in header:
            if key in item:
                worksheet.write(row,col,str(item[key]))
            col+=1

    workbook.close()

def writeDataCsv(header,items,filename = 'cachedata.csv'):
    with open(filename,'a+',encoding='utf8') as file:
        f_csv = csv.DictWriter(file, header)
        f_csv.writeheader()
        f_csv.writerows(items)
            

     
if __name__ == '__main__':
    pass

    

  
    

