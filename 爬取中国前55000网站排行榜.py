#coding=utf-8
import requests
from lxml import etree
#http://top.chinaz.com/all/
# import vthread
import random
import time
# @vthread.pool(40)
def get_urls(url):
    s = requests.get(url,timeout=6)
    html = etree.HTML(s.content)
    urls=[]
    for i in range(30):
        a = html.xpath("/html/body/div[3]/div[3]/div/ul/li["+str(i)+"]/div[2]/h3/span")
        b=html.xpath("/html/body/div[3]/div[3]/div/ul/li["+str(i)+"]/div[2]/p")
        for j in a:
            urls.append(j.text)
        for k in b:
            urls.append(k.text)
    # print(urls)
    return urls

urls=[]
url_1="http://top.chinaz.com/all/"
temp_list=get_urls(url_1)
for i in temp_list:
    urls.append(i)

# http://top.chinaz.com/all/index_3.html
for i in range(2,1916):
    print("第{}个".format(i))
    # str(round(random.uniform(1, 2), 1))
    #请求间隔可以适当增大
    # time.sleep(random.randint(1,2))
    time.sleep(0.2)
    try:
        url = "http://top.chinaz.com/all/index_" + str(i) + ".html"
        temp_list = get_urls(url)
        for i in temp_list:
            urls.append(i)
    except:
        pass


with open("results.txt","w+") as f:
    m=2
    for i in urls:
        try:
            f.write(i)
            f.write("  ")
        except:
            pass
        if m % 2==1:
            f.write("\n")
        # else:
            # print(i)
        m = m + 1
f.close()