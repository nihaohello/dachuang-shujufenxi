#coding=utf-8
import re
import requests
import os
rootdir="/root/temp/data/"
list_txt = os.listdir(rootdir)
# print(list_txt)
for i in list_txt:
    f=open(rootdir+i)
    s = f.read().decode('utf8')
    f.close()
    m = re.findall(u'[\u4e00-\u9fa5]+', s)
    with open(rootdir+i,"w+") as f:
        for i in m:
            f.write(i.encode("utf-8"))
            f.write("\n")