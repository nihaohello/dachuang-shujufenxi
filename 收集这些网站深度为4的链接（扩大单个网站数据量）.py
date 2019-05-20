# coding=utf-8
import requests
import re
from urllib.parse import urlparse
from urllib import parse
import sys
import os
import vthread
import random
import multiprocessing
import threading
import MySQLdb
mutlx1=threading.Lock()
class crawl(object):
    def __init__(self, urls):
        self.urls = urls
        self.collect_url = []
        self.domain_collect_url=[]
        self.sql_xss_collect_url=[]
        self.file_name = "target_"
        self.num=random.randint(3,4)
    def run(self):
        # self.db = MySQLdb.connect("localhost", "root", "root", "AI", charset='utf8')
        # self.cursor = self.db.cursor()
        for url in self.urls:
            b = self.deal_url(url)
            a = b[1].split(".")
            Is_url=a[-2]+"."+a[-1]
        #print(self.Is_url)
            num = 0
            self.crawl(url,num,Is_url)
        #self.file_fave()
    @vthread.pool(40)
    def crawl(self, url, num,Is_url):
        print(url)
        temp_collect_urls=[]
        temp_urls=self.deal_url(url)
        try:
            temp_url=temp_urls[0]+"://"+temp_urls[1]
        except Exception:
            pass
        num = num + 1
        #print(num)
        if num <= self.num:
            try:
                s = requests.get(url=url, timeout=6)
            except requests.RequestException.ConnectTimeout:
                url=url.lstrip("http")
                url="https"+url
                s = requests.get(url=url, timeout=6)
            urls1 = re.findall('href=".*?"', s.text)
            urls2 = re.findall("href=\'.*?\'", s.text)
            urls3 = re.findall('src=".*?"', s.text)
            urls4 = re.findall("src=\'.*?\'", s.text)
            # urls=re.findall('.*?'+self.Is_url+".*?",s.text)
            urls = urls1 + urls2 + urls3 + urls4
            # print(urls)
            if urls:
                for i in urls:
                    if Is_url in i:
                        i = self.deal_href_src(i)
                        if "http" not in i:
                            i = "http://" + i
                        # print(i)
                    if Is_url not in i:
                        i = self.deal_href_src(i)
                        if "http" not in i:
                            i = temp_url + "/" + i
                    if "javascript" not in i and i not in self.collect_url and "JavaScript" not in i:
                        if ((".png" not in i) and (".jpg" not in i and \
                                                   (".gof" not in i) and (".css" not in i) and ((".js" not in i) or \
                                                                                                (".json" in i)) and (
                                                           ".ico" not in i) and "/css/" not in i and "/js/" \
                                                   not in i and \
                                                   ".jpeg" not in i and ".svg" not in i and "ä" not in i)):
                            if Is_url in i and i not in self.collect_url:
                                temp_collect_urls.append(i)
                    if temp_collect_urls:
                        mutlx1.acquire()
                        self.collect_url = self.collect_url + temp_collect_urls
                        mutlx1.release()
                        for i in temp_collect_urls:
                            print(i)
                            # a = i
                            # a = "'" + a + "'"
                            # sql = "insert into urls (urls) values (%s)" % (a)
                            # self.cursor.execute(sql)
                            # self.db.commit()
                            # self.crawl(i, num, Is_url)
                    temp_collect_urls = []
    def deal_url(self,url):
        return urlparse(url)
    def deal_href_src(self,i):
        i=parse.unquote(i)
        if "href=" in i:
            i = i.rstrip("\"").lstrip('href=')
            i = i.rstrip("\'").lstrip('href=')
            i = i.strip("\"")
            i = i.rstrip("/")
        if "src" in i:
            i = i.lstrip("src=").rstrip("\"")
            i = i.lstrip("\"")
            i = i.rstrip("/")
        i=i.replace("'","")
        i=i.strip(".").strip("/")
        return i
    # def file_fave(self):
    #     mutlx1.acquire()
    #     with open(self.file_name+"total.txt","a+",encoding="utf-8") as f:
    #         for url in self.collect_url:
    #             f.write(url)
    #             f.write("\n")
    #     f.close()
    #     mutlx1.release()
if __name__ == '__main__':
    f = open("china_top450_url.txt", encoding="utf-8")
    urls = []
    for url in f.readlines():
        if not url.startswith("http"):
            url = "http://www." + url
        url = url.rstrip("\n")
        urls.append(url)
    crawl(urls).run()
    f.close()



