import requests
import json

para = 'jQuery111307589481875766069_1516516559149'
id = 1474441961853

#url = 'http://www.gzdata.gov.cn/dataopen/api/dataset/1474441961853/filedata?callback=jQuery111307589481875766069_1516516559149&_=1516516559150'
#url = 'http://www.gzdata.gov.cn/dataopen/api/filedata/1474264646836?callback=jQuery111307589481875766069_1516516559145&_=1516516559151'
url = 'http://www.gzdata.gov.cn/dataopen/api/url/A3QVb2mUnUFrR3UFrefyyIz2?callback=jQuery111307589481875766069_1516516559145&_=1516516559152'

with open('cookie00.txt') as f:
    cookie = f.read()
cookies = json.loads(cookie)

timeout =3

response = requests.get(url,cookies=cookies,timeout=timeout)
print(response.text)


