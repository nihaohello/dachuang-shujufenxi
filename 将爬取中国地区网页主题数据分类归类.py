#coding=utf-8
import jieba
from gensim import corpora,models,similarities
import time
start_time=time.time()
#得到停用词
def stop_words(stop_word_file):
    with open(stop_word_file) as fp:
        words = fp.read()
        # print(words)
        result = words.split('\n')
    return result
stop_file_name = "/root/temp/data/stopwordlist.txt"
stopwords = stop_words(stop_file_name)
#删除停用词
def del_stop_words(words,stop_words_set):
    new_words = []
    for k in words:
        if k not in stop_words_set:
            new_words.append(k)
    return new_words


#从文件得到网址与主题
all_doc=[]
f=open("url_content_data.txt")
for i in f.readlines():
    i=i.rstrip("\n")
    # i=del_stop_words(i,stopwords)
    all_doc.append(i)
f.close()
# print(all_doc)

def return_xiangshidu_dayu_0_65(doc_test,all_doc,all_url):
    # doc_test = "我喜欢上海的小吃"
    # all_doc = []
    all_doc_list = []
    for doc in all_doc:
        doc_list = [word for word in jieba.cut(doc)]
        all_doc_list.append(doc_list)
    # print(all_doc_list)
    # 以下把测试文档也进行分词，并保存在列表doc_test_list中
    doc_test_list = [word for word in jieba.cut(doc_test)]
    # 首先用dictionary方法获取词袋（bag-of-words)
    dictionary = corpora.Dictionary(all_doc_list)
    # 词袋中用数字对所有词进行了编号
    # print(dictionary.keys())
    # 编号与词之间的对应关系
    # print(dictionary.token2id)
    # 以下使用doc2bow制作语料库
    # 语料库是一组向量，向量中的元素是一个二元组（编号、频次数），对应分词后的文档中的每一个词。
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
    # 以下用同样的方法，把测试文档也转换为二元组的向量
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    tfidf = models.TfidfModel(corpus)
    # 获取测试文档中，每个词的TF-IDF值
    # tfidf[doc_test_vec]
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
    sim = index[tfidf[doc_test_vec]]
    temp_list = sorted(enumerate(sim), key=lambda item: -item[1])
    # print(temp_list)
    # print(type(temp_list))
    tem_num=[]
    for i in temp_list:
        # print(type(i))
        if i[1] > 0.3:
            tem_num.append(i[0])
            # print(all_doc[7])
    tem_urls=[]
    for i in tem_num:
        tem_urls.append(all_url[i].strip())
    return tem_urls

all_urls=[]
all_docs=[]
for i in all_doc:
    if "网站简介：" in i:
        all_urls.append(i.split("网站简介：")[0].strip())
        # print(i.split("网站简介：")[0])
        all_docs.append(i.split("网站简介：")[1].strip())
        # print(i.split("网站简介：")[1])
# print(all_urls)
sum_urls=[]
reslusts_urls=[]
for i in range(len(all_docs)):
    doc_test=all_docs[i]
    doc_test_url=all_urls[i]
    if doc_test_url not in sum_urls:
        a=return_xiangshidu_dayu_0_65(doc_test,all_docs,all_urls)
        reslusts_urls.append(a)
        for j in a:
            if j not in sum_urls:
                sum_urls.append(j)
# print(len(sum_urls))
# print(sum_urls)
# print(reslusts_urls)
with open("results_urls_fenlei.txt","w+") as f:
    for i in reslusts_urls:
        f.write(str(i))
        f.write("\n")
f.close()
print("一共有{}个类别".format(len(reslusts_urls)))
print("耗时{}".format(time.time()-start_time))
