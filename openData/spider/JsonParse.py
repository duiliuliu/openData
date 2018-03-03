# *-* encoding = utf-8 *-* 
# author: pengr

'''将字典的多层嵌套转化为一层 '''
'''将json压扁成一层字典'''
'''
    写入Excel文件时，表格第一行数据可以是 获取items的key集合，存储set，然后不断update
'''

class JsonParse(object):
    def __init__(self, ):
        self.dict={}


    '''对列表进行遍历'''
    '''
        .   如果列表内元素只有一个，则去列表
        .   列表元素多个，解析列表元素，平展化列表内部元素
    '''
    def parseList(self,content):
        if len(content)==1:
            return self.parse(content[0])
        else:
            subcata = []
            subcata.append('子元素：')
            for item in content:
                subcata.append(self.parse(item))
            return subcata
    

    '''对字典进行遍历'''
    '''
        .   将字典子元素嵌套字典的，去嵌套，并且该元素的值为 子元素键的列表集合
    '''
    def parseDict(self,content):
        subcata = []
        subcata.append('子属性：')
        for key,value in content.items():
            subcata.append(key)
            if type(value) == dict or type(value) == list:
                self.dict[key] = self.parse(value)
                #parse将返回key的集合，赋值给该元素
            else:
                if key in self.dict:
                    if type(self.dict[key]) == list:
                        self.dict[key].append(value)
                    else:
                        l = []
                        l.append(self.dict[key])
                        l.append(value)
                        self.dict[key] = l
                else:
                    self.dict[key] = value
        return subcata


    def parse(self,content):
        if type(content) == list:
            return self.parseList(content)
        if type(content) == dict:
            return self.parseDict(content)

    def getItems(self):
        return self.dict

    def getKeys(self):
        return [key for key in self.dict.keys()]

    def getHeaders(self):
        header = {}
        for k,v in self.dict.items():
            try:
                if '子属性：' in v:
                    header[k] = v[1:]
                else:
                    header[k] = ''
            except:
                header[k] = ''
        return header
            

if __name__ == '__main__':
    parse = JsonParse()
    strlist = [{'creator': '1', 'creator_name': 'null', 'conf_released_time': 1506688277000, 'cata_title': '个人荣誉信息', 'description': '个人荣誉信息', 'cata_id': '80866', 'cata_tags': '姓名,授予日期,授予单位,荣誉称号,时间,荣誉,表彰文号,授予,单位,个人,更新时间,更新,信息,日期,表彰,文号', 'cata_code': 'ml_fs_kf_zw_swgxj_011', 'conf_extend_field': None, 'conf_cata_magnitude': '1', 'catalogStatistic': {'use_task_count': 0,
'use_points': 0, 'file_count': 3, 'update_time': None, 'use_visit': 864, 'data_count': 11, 'task_count': 0, 'use_grade': 0.0, 'audience_type': None, 'use_data_count': 0, 'use_scores': 0, 'use_favs': 1, 'api_count': 0, 'cata_id': None, 'use_api_count': 0, 'use_comments': 0, 'use_file_count': 0, 'apply_count': None}, 'cataLogIndustrys': [{'group_id': 'ind-18', 'link_id': '81322', 'update_time': None, 'group_type': '20', 'group_name': '文化、体育和娱乐业', 'cata_id': '80866', 'description': None}], 'conf_create_time': 1498802493000, 'cata_encryption_level': None, 'conf_update_cycle': '7', 'shared_type': '2', 'conf_catalog_format': '1,2,3', 'conf_use_type': '1,2,3,', 'update_time': '2017-09-29 20:30:10', 'standard_id': None, 'open_type': '无条件开放', 'conf_data_scope': None, 'conf_datafile_generate_rule': None, 'org_code': '4406003017', 'cata_language': '', 'open_scope': None, 'conf_download_enable': None, 'status': 2, 'type_code': None, 'conf_status': '4', 'cata_version': None, 'conf_update_time': 1506688210000, 'org_name': '文广新局', 'cataLogGroups': [{'group_id': 'sub-7', 'link_id': '81321', 'update_time': None, 'group_type': '10', 'group_name': '文化休闲', 'cata_id': '80866', 'description': None}], 'columns': None, 'cata_items': '姓名|荣誉', 'conf_update_cycle_user': '', 'subject_cata_type': None, 'shared_scope': None, 'cata_logo': 'http://www.fsdata.gov.cn/rcservice/doc?doc_id=2780', 'contact_email': '', 'region_code': '440600', 'conf_data_update_time': 1506149807000, 'contact_phone': '', 'conf_is_view': 0, 'conf_datafile_sample_num': 0, 'released_time': '2017-09-29 20:31:17', 'conf_datafile_update_time': 1507618805000, 'parent_id': None, 'conf_contact_ispublic': None, 'conf_offline_time': 1506688163000, 'conf_join_type': None, 'deleteColumnIds': None, 'cataLogConfigures': None, 'conf_datafile_type': '0', 'contact_name': '', 'cata_type': '10'}]
    parse.parse(strlist)
    print(parse.getItems())
    