#   *-* encoding = utf-8 *-*
#   author: pengr

'''深圳市资源目录'''

from spider import Spider,Writer


'''处理请求的数据'''
def func(response = None, data=None ,header=None ):
    if response:
        return response.json()['result']

    if data:
        print(data)

    if header:
         pass


if __name__ == '__main__':
    '''深圳  160页'''
    page = 1
    urls = []
    for pageNo in range(1,page):
        url = "http://opendata.sz.gov.cn/dataapi/queryDataApi"
        urls.append(url)
    
    data
    szSpider = Spider.Spider()
    szSpider(urls,method = 'post', func = func)

    filexlsx = 'source/szdata.xlsx'
    Writer.writeDataExcel(szSpider.tableHeader,szSpider.data,filename=filexlsx)