#   *-* encoding = utf-8 *-*
#   author: pengr

'''哈尔滨资源目录'''

from spider import Spider,Writer
import re
import os,requests
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool #多线程

def func(response = None,  data=None, header = None):
    if response:
        return response.json()['data']

    if data:
        for item in data:
             
            item['description'] = ''.join(item['description'].split(' '))
            
            #获取到的更新频率与数据格式为编号，转化编号
            if item['update_cycle'] == '4':
                item['update_cycle'] = '每月'
            elif item['update_cycle'] == '7':
                item['update_cycle'] = '每年'
            else:
                item['update_cycle'] = '不详'
                
            format_list = item['use_type'].strip().split(',')
            format_dict = {
                '1':'数据集',
                '2':'文件集',
                '3':'API服务',
                '4':'地图',
                '':''
            }
            tmp = []
            for l in format_list:
                tmp.append(format_dict[l])
            item['use_type'] = ' '.join(tmp)

            #所属主题与所属行业所标识的键为同一键
            name = item['group_name'].split(',',1)
            item['topic_name'] = re.sub('\w+\-\d+:\d+:','',name[0])
            item['group_name'] = re.sub('\w+\-\d+:\d+:','',name[1])
                

    if header:
        myheader = {
            'cata_id':'id',
            'cata_title':'数据目录名称',
            'data_count':'数据量',
            'file_count':'文件数',
            'api_count':'接口数量',
            'open_type':'开放状态',
            'topic_name':'所属主题',
            'update_time':'最后更新',
            'org_name':'来源部门',
            'cata_tags':'标签',
            'update_cycle':'更新频率',
            'use_type':'数据格式',
            'released_time':'发布时间',
            'group_name':'所属行业',
            'description':'简介',
            'use_file_count':'下载次数',
            'use_visit':'浏览次数',
            'use_grade':'评分人数',
            'use_task_count':'评价次数',
            'use_points':'评分总数',
            'use_scores':'平均评分',
            'data_count':'数据条目',
            'download_url':'下载URL http://data.harbin.gov.cn/odweb/catalog/catalogDetail.do?method=getFileDownloadAddr&fileId=',
            'download_file':'文件名称',
            'download_size':'文件大小',
            'header_sort':['cata_title','cata_id','data_count','download_url','download_file','download_size',
                'data_count','file_count','api_count','open_type','topic_name','update_time','org_name','cata_tags',
                'update_cycle','use_type','released_time','group_name','description','use_file_count','use_visit','use_grade',
                'use_task_count','use_points','use_scores'
            ]
        }

        header['download_url'] = ''
        header['download_file'] = ''
        header['download_size'] = ''
        header['data_count'] = ''
        header['topic_name'] = ''
        header['myheader'] = myheader
 

def downloadfile(data):  
    print('\t-------'+data['cata_id'])
    url = 'http://data.harbin.gov.cn/odweb/catalog/catalogDetail.htm?cata_id={}'.format(data['cata_id']) 
    response = requests.get(url)
    htm = html.fromstring(response.text)
    res = htm.xpath('//div[@class="download-list"]/ul/li/div[2]/a/@id') 
    download_file = htm.xpath('//div[@class="download-list"]/ul/li/div[2]/a/text()')
    download_file = [re.sub('\s.*?$','',i.strip()) for i in download_file if i.strip() != ''] 
    # print(download_file[0])

    url_pre = 'http://data.harbin.gov.cn/odweb/catalog/catalogDetail.do?method=getFileDownloadAddr&fileId='
    download_url = [url_pre+i for i in res] 
 
    data['download_url'] = ' '.join([i for i in res])
    data['download_file'] = ' '.join(download_file)   
 
    dir = os.getcwd()+'/source/hrb/'+re.sub('[/\\:\*\?<>|"\']','', data['cata_title'])
    if not os.path.exists(dir):
        os.mkdir(dir)
    for url,file in zip(download_url,download_file):
        if os.path.exists(dir+'/'+file):
            continue

        res = requests.get(url)  
        with open(dir+'/'+file,'wb+') as f:
            f.write(res.content)
 

if __name__ == '__main__':
    ''' 哈尔滨数据 135页'''
    page = 135
    urls = []
    for start in range(page):
        start *= 6
        url="http://data.harbin.gov.cn/odweb/catalog/catalog.do?method=GetCatalog&group_id&org_code&start="+str(start)+"&length=6&pageLength=6&cata_type=default&keywords"
        urls.append(url)
    hrbSpider = Spider.Spider()
    hrbSpider(urls,method = 'post',func = func)

    path = os.getcwd()
    dir = path+'/source/hrb'
    if not os.path.exists(dir):
        os.mkdir(dir)


    print('\n'.join(['-'*40,'\t下载全部资源','-'*40]))
    
    pool = ThreadPool(processes = 6)
    pool.map(downloadfile, hrbSpider.data)
    pool.close() # 关闭进程池，表示不能在往进程池中添加进程
    pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用
 
    # downloadfile(hrbSpider.data[0])


    filexlsx = 'source/hrbdata.xlsx'
    Writer.writeDataExcel(hrbSpider.tableHeader,hrbSpider.data,filename=filexlsx)
    # Writer.writeDataMongo(hrbSpider.tableHeader,hrbSpider.data,collection_name='db.hrb_catalog')
    print('\tend!')
