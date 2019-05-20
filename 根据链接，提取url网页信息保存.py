#coding=utf-8
import requests
from urllib.parse import urlparse
from urllib import parse
import re
from os import path
import vthread
f=open("test_urls_.txt")
def deal_url(url):
    return urlparse(url)
@vthread.pool(40)
def requests_url(url,tmp_name):
    try:
        s = requests.get(url=url, timeout=6)
    except Exception as e:
        url = url.lstrip("http")
        url = "https" + url
        s = requests.get(url=url, timeout=6)
    if True:
        with open("/root/temp/data/"+tmp_name+".txt", "a+") as f:
            f.write(s.text)
            f.write("\n")
        f.close()
for url in f.readlines():
    url=url.rstrip("\n")
    try:
        tmp_name=deal_url(url)[1].split(".")[1]
    except Exception as e:
        tmp_name="tmp_text"
    print(url)
    if re.match(r'^https?:/{2}\w.+$', url) or re.match(r'^http?:/{2}\w.+$', url):
        requests_url(url,tmp_name)



