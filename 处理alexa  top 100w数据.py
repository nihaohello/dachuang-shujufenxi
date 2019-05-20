#coding=utf-8
import csv
#函数来自《Web安全之机器学习入门》
def load_alexa(filename):
    domain_list=[]
    csv_reader = csv.reader(open(filename))
    for row in csv_reader:
        domain=row[1]
        if domain >= 10:
            domain_list.append(domain)
    return domain_list
domain_list=load_alexa(r"top-1m.csv")
with open("top-1m.txt",'w+') as f:
    for i in domain_list:
        f.write(i)
        f.write("\n")
f.close()

