# *-* encoding = utf-8 *-* 
# author: pengr

from spider import Spider,Writer
import time

def func(response = None,  data=None, header = None):
    if response:
        return response.json()['data']

    if data:
        tmp = []
        for i in data[0]['update_time']:
            if i:
                tmp.append(i)
        data[0]['update_time'] = tmp

    if header:
        myheader = {
            'cata_title':'数据目录名称',
            'data_count':'数据量',
            'file_count':'文件数',
            'api_count':'接口数量',
            'open_type':'开放状态',
            'group_name':'经济建设',
            'update_time':'最后更新',
            'org_name':'来源部门',
            'cata_tags':'标签',
            'released_time':'发布时间',
            'group_name':'所属行业',
            'description':'简介',
            'use_file_count':'下载次数',
            'use_visit':'浏览次数',
            'use_grade':'评分人数',
            'use_task_count':'评价次数',
            'use_points':'评分总数',
            'use_scores':'平均评分',
            'header_sort':[
                'cata_title','data_count','file_count','api_count','open_type','group_name','update_time','org_name',
                'cata_tags','released_time','group_name','description','use_file_count','use_visit','use_grade','use_task_count',
                'use_points','use_scores'
            ]
        }

        header['myheader'] = myheader
        
def gettime(timestamp):
    try:
        timestamp = timestamp /1000
        time_local = time.localtime(timestamp)
        return time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    except :
        return timestamp
    

if __name__ == '__main__':
    ''' 佛山数据  66页'''
    page = 66
    urls = []
    for start in range(page):
        url="http://www.fsdata.gov.cn/data/catalog/catalog.do?method=GetCatalog&data={&_order=cc.update_time desc&org_code&group_id&use_type&catalog_format&keywords&tag&grade&cata_type=default&start="+str(start)+"&length=6&pageLength=6&}"
        urls.append(url)
    fsSpider = Spider.Spider()
    fsSpider(urls,method = 'post',func = func)
    #filecsv = 'source/fsdata.csv'
    #Writer.writeDataCsv(fsSpider.tableHeader,fsSpider.data,filename=filecsv)

    filexlsx = 'source/fsdata.xlsx'
    Writer.writeDataExcel(fsSpider.tableHeader,fsSpider.data,filename=filexlsx)