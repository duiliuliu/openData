# *-* encoding = utf-8 *-* 
# author: pengr

from spider import Spider
import time

def func(response = None,  data=None, header = None):
    if response:
        return response.json()['data']

    if data:
        for item in data:
            for key in item.keys():
                if 'time' in key:
                    item[key] = gettime(item[key])
        
def gettime(timestamp):
    try:
        timestamp = timestamp /1000
        time_local = time.localtime(timestamp)
        return time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    except :
        return timestamp
    

if __name__ == '__main__':
    ''' 佛山数据 '''
    page = 66
    urls = []
    for start in range(page):
        url="http://www.fsdata.gov.cn/data/catalog/catalog.do?method=GetCatalog&data={&_order=cc.update_time desc&org_code&group_id&use_type&catalog_format&keywords&tag&grade&cata_type=default&start="+str(start)+"&length=6&pageLength=6&}"
        urls.append(url)
    fsSpider = Spider.Spider()
    fsSpider(urls,method = 'post',func = func)
    filecsv = 'source/fsdata.csv'
    filexlsx = 'source/fsdata.xlsx'
    Spider.writeDataCsv(fsSpider.tableHeader,fsSpider.data,filename=filecsv)
    Spider.writeDataExcel(fsSpider.tableHeader,fsSpider.data,filename=filexlsx)