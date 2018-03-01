#encoding = utf8
import requests
from bs4 import BeautifulSoup
import re
 
  
User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent
  
'''
获取所有代理IP地址
'''
def getProxyIp():
    proxy = []
    for i in range(1,2):
        try:
            url = 'http://www.xicidaili.com/nn/'+str(i)
            req = requests.get(url,headers=header).text
            soup = BeautifulSoup(req,'lxml')
            ips = soup.findAll('tr')
            for x in range(1,len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]
                proxy.append(ip_temp)
        except:
            continue
    return proxy

'''
验证获得的代理IP地址是否可用
'''
def validateIp(proxy):
    url = "http://ip.chinaz.com/getip.aspx"
    f = open("ip.txt","w")
    timeout = 3
    for i in range(0,len(proxy)):
        try:
            ip = proxy[i].strip().split("\t")
            proxy_host = "http://"+ip[0]+":"+ip[1]
            proxy_temp = {"http":proxy_host}
            res = requests.get(url,proxies = proxy_temp,timeout = timeout)
            if re.match('\{.*?\}',res.text):
                f.write(proxy_host+'\n')
                print(proxy[i])
        except :
            continue
    f.close()


if __name__ == '__main__':
    proxy = getProxyIp()
    validateIp(proxy)