# *-* encoding = utf-8 *-* 
# author: pengr

import json
import requests
import re

with open('cookie.txt','r',encoding='utf-8') as f:
    cookie=f.read()
cookies=json.loads(cookie)
header={
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.6.2.15784"
}

url = 'http://www.gzdata.gov.cn/dataopen/api/filedata/1474264646836?callback=jQuery111309967397004365921_1512390694429&_=1512390694437'
response = requests.get(url,cookies=cookies,headers = header)
response = str(response.content,'utf-8')
response = re.sub("/\*\*/\w+\d+\(",'',response)
response = re.sub('\);','',response)
response = json.loads(response)
print('-'*20)
para = response['data']['shortUrl']
print(para)

url = 'http://www.gzdata.gov.cn/dataopen/api/url/'+para+'?callback=jQuery111309967397004365921_1512390694429&_=1512390694438'
#url = 'http://www.gzdata.gov.cn/dataopen/api/url/A3QVb2mUnUFrR3UFrefyyIz2?callback=jQuery111306425414993427694_1512461832121&_=1512461832132'
response = requests.get(url,cookies=cookies,headers = header)

response = str(response.content,'utf-8')
response = re.sub("/\*\*/\w+\d+\(",'',response)
response = re.sub('\);','',response)
response = json.loads(response)
print('-'*20)
print(response)

url = response['data']['realUrl']
#url = 'http://gzopen.oss-cn-guizhou-a.aliyuncs.com/201401.docx?Expires=1790350958&OSSAccessKeyId=cRMkEl0MLhpV9l7g&Signature=dB8Riw3q22RD2nWNh1MWekT73zc%3D'
response = requests.get(url)
with open('ss.docx','wb') as code:
    code.write(response.content)



