#coding=utf-8
import requests
import re
from lxml import etree
url_1="http://alexa.chinaz.com/Country/index_CN.html"
url="http://alexa.chinaz.com/Country/index_CN"
def deal_html(i):
    s = requests.get(i)
    html = etree.HTML(s.content)
    for p in range(25):
        a = html.xpath("/html/body/div[2]/div[4]/ul/li[" + str(p) + "]/div[2]/h3/a[1]")
        for j in a:
            print(j.text)
deal_html(url_1)
for i in range(2,20):
    i=url+"_"+str(i)+".html"
    deal_html(i)

# http://alexa.chinaz.com/Country/index_CN.html
# /html/body/div[2]/div[4]/ul/li[1]/div[2]/h3/a[1]
# /html/body/div[2]/div[4]/ul/li[2]/div[2]/h3/a[1]