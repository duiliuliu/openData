# *-* encoding = utf-8 *-* 
# author: pengr

import requests
import re
from lxml import html
import queue
import threading

exitFlag = 0
ip_list = []
port_list = []

headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.6.2.15784'
}

for i in range(1,5):
    url = 'http://www.xicidaili.com/nn/'+str(i)
    #print(url)
    response = requests.get(url,headers=headers).text
    #print(response)


    ip_pattern = re.compile('<td.*?>(\d{2,3}.\d+.\d+.\d+)</td>')
    port_pattern = re.compile('<td.*?>(\d+)</td>')

    ip_l = re.findall(ip_pattern,response)
    port_l = re.findall(port_pattern,response)

    ip_list.extend(ip_l)
    port_list.extend(port_l)

print('-'*20)
print(len(ip_list))
print(len(port_list))

proxies_list = []
workQueue = queue.Queue(len(ip_list))
queueLock = threading.Lock()

print(workQueue)

queueLock.acquire()
for ip,port in zip(ip_list,port_list):
    proxies ={'http':'http://'+ip+":"+port}
    workQueue.put(proxies)
queueLock.release()


class MyThread(threading.Thread):
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id = id
    def run(self):
        print("开始线程"+str(self.id))
        request()
        print("结束线程"+str(self.id))

   
def request():
    timeout = 2
    while not exitFlag:
        try:
            url = "http://ip.chinaz.com/getip.aspx" 
            proxies = workQueue.get()
            response = requests.get(url,proxies=proxies, timeout=timeout)
            print(response.text) 
            proxies_list.append(proxies)
        except :
            print(proxies)
            print('===='+"无效")

threads = []

for i in range(10):
    thread = MyThread(i)
    thread.start()
    threads.append(thread)

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

for thread in threads:
    thread.join()

with open('dali.txt','a+') as f:
    for i in 