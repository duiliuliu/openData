# *-* encoding = utf-8 *-* 
# author: pengr

'''佛山基础数据资源目录'''

from spider import Spider,Writer
import os
import requests 
import multiprocessing

def func(response = None,  data=None, header = None):
    if response:
        return response.json()['data']

    if data:
        for item in data:
            #获取到的更新时间有空值与重复值
            item['update_time'] = mytrim(item['update_time'])

            #去除简介空值
            item['description'] = mytrim(item['description'])

            #去除ID空值
            item['cata_id'] = item['cata_id'][0]
            
            #获取到的更新频率与数据格式为编号，转化编号
            if item['conf_update_cycle'] == '4':
                item['conf_update_cycle'] = '每月'
            elif item['conf_update_cycle'] == '7':
                item['conf_update_cycle'] = '每年'
            elif item['conf_update_cycle'] == '5':
                item['conf_update_cycle'] = '每季度'
            elif item['conf_update_cycle'] == '2':
                item['conf_update_cycle'] = '每天'
            elif item['conf_update_cycle'] == '6':
                item['conf_update_cycle'] = '每半年'
            elif item['conf_update_cycle'] == '8':
                item['conf_update_cycle'] = '实时'
            elif item['conf_update_cycle'] == '1':
                item['conf_update_cycle'] = '自定义'
                
            format_list = item['conf_use_type'].strip().split(',')
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
            item['conf_use_type'] = ' '.join(tmp)

            #所属主题与所属行业所标识的键为同一键
            if type(item['group_name']) == list:
                item['topic_name'] = item['group_name'][1]
                item['group_name'] = item['group_name'][0]
            else:
                item['topic_name'] = item['group_name']
                item['group_name'] = ''
                

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
            'conf_update_cycle':'更新频率',
            'conf_use_type':'数据格式',
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
            'download_url':'下载URL',
            'download_file':'文件名称',
            'download_size':'文件大小',
            'header_sort':['cata_id','data_count','download_url','download_file','download_size',
                'cata_title','data_count','file_count','api_count','open_type','topic_name','update_time','org_name','cata_tags',
                'conf_update_cycle','conf_use_type','released_time','group_name','description','use_file_count','use_visit','use_grade',
                'use_task_count','use_points','use_scores'
            ]
        }

        header['topic_name'] = ''
        header['myheader'] = myheader
 
#去除空值
def mytrim(item):
    tmp = []
    for i in item:
        if i:
            tmp.append(i)
    return ' '.join(tmp)   

def downloadfile(data): 
    print('\t-------'+data['cata_id'])
    url = 'http://www.fsdata.gov.cn/data/catalog/catalogDetail.do?method=GetDownLoadInfo'
    para = {
        'cata_id':'43270',
        'conf_type':'2'
    } 
    response = requests.post(url,data=para)
    res = response.json()

    url_pre = 'http://www.fsdata.gov.cn/data/catalog/catalogDetail.do?method=getFileDownloadAddr&fileId='
    download_url = [url_pre+i['fileId'] for i in res['data']]
    download_file = [i['fileName'] for i in res['data']]

    data['data_count'] = res['data'][0]['dataCount'] 
    data['download_url'] = ' '.join(download_url)
    data['download_file'] = ' '.join(download_file)
    data['download_size'] = ' '.join([str(i['fileSize']) for i in res['data']])
 
    dir = os.getcwd()+'/source/fs/'+data['cata_title']
    if not os.path.exists(dir):
        os.mkdir(dir)
    for url,file in zip(download_url,download_file):
        res = requests.get(url)  
        with open(dir+'/'+file+'.zip','wb+') as f:
            f.write(res.content)


if __name__ == '__main__':
    ''' 佛山数据  66页'''


    page = 66
    urls = []
    for start in range(page):
        start *= 6
        url="http://www.fsdata.gov.cn/data/catalog/catalog.do?method=GetCatalog&data={&_order=cc.update_time desc&org_code&group_id&use_type&catalog_format&keywords&tag&grade&cata_type=default&start="+str(start)+"&length=6&pageLength=6&}"
        urls.append(url)
    fsSpider = Spider.Spider()
    fsSpider(urls,method = 'post',func = func)

    path = os.getcwd()
    dir = path+'/source/fs'
    if not os.path.exists(dir):
        os.mkdir(dir)


    print('\n'.join(['-'*40,'\t下载全部资源','-'*40]))
    
    pool = multiprocessing.Pool(processes = 6)
    pool.map(downloadfile, fsSpider.data)
    pool.close() # 关闭进程池，表示不能在往进程池中添加进程
    pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用
 
    # downloadfile(fsSpider.data[0])

    
    #filecsv = 'source/fsdata.csv'
    #Writer.writeDataCsv(fsSpider.tableHeader,fsSpider.data,filename=filecsv) 
    filexlsx = path+'/source/fsdata.xlsx'
    Writer.writeDataExcel(fsSpider.tableHeader,fsSpider.data,filename=filexlsx)
    # Writer.writeDataMongo(fsSpider.tableHeader,fsSpider.data,collection_name='db.fs_catalog')
    print('\tend!')


    
 


''' 佛山的下载URL获取之后，无论有没有登录，都可以下载，所以完全不需要下载资源，而是存储URL即可 '''