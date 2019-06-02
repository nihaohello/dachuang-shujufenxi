#coding=utf-8
import re
import jieba
import jieba.analyse  # 提取关键内容
import jieba.posseg as pseg  # 词性标注
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics.pairwise import cosine_similarity
from snownlp import SnowNLP
from scipy.misc import imread
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer # 基于TF-IDF的词频转向量库
from sklearn.manifold import TSNE
from pandas import DataFrame
import pandas as pd
def read_from_file(file_name):
    with open(file_name) as fp:
        words = fp.read()
    return words


def cut_words(words):
    result = jieba.cut(words)
    words = []
    for r in result:
        words.append(r)
    return words


def stop_words(stop_word_file):
    with open(stop_word_file) as fp:
        words = fp.read()
        # print(words)
        result = words.split('\n')
    return result

read_file_name="data_test.txt"
stop_file_name="/root/temp/data/stopwordlist.txt"
listall=read_from_file(read_file_name)
stopwords = stop_words(stop_file_name)
def del_stop_words(words,stop_words_set):
    new_words = []
    for k in words:
        if k not in stop_words_set:
            new_words.append(k)
    return new_words

# for a in listall:
#     list0.extend(del_stop_words(cut_words(a),stopwords))
list0 = []
#去除停用词
list0 = del_stop_words(cut_words(listall),stopwords)
listall1 = list(set(list0))
listall1.sort(key = list0.index)
comment_list=listall1
# print(listall1)


vectorizer = CountVectorizer()
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectorizer.fit_transform(listall1))


word = vectorizer.get_feature_names()
# print("word feature length: {}".format(len(word)))

tfidf_weight = tfidf.toarray()


def KMeans_function(tfidf_weight,word,clusters=1):
    clf_KMeans = KMeans(n_clusters=clusters)
    clf_KMeans.fit(tfidf_weight)

    clf_KMeans_label = clf_KMeans.labels_  # 获取聚类标签
    clf_KMeans_cluster_centers_ = clf_KMeans.cluster_centers_  # 获取聚类中心
    clf_KMeans_inertia = clf_KMeans.inertia_  # 获取聚类准则的总和

    res0Series = pd.Series(clf_KMeans.labels_)
    # print(res0Series)

    quantity=pd.Series(clf_KMeans.labels_).value_counts()
    print("cluster2聚类数量:")
    print(quantity)
    order_centroids=clf_KMeans_cluster_centers_.argsort()
    # print(type(order_centroids))
    # for i in order_centroids:
    #     for j in i:
    #         print(j)
    for i in range(6):
        print(word[order_centroids[0][i]],end=' ')
    print("\n")
    # print(order_centroids)
    # for i in (clusters):
    #     print(word[i],end='')
    #     print()


KMeans_function(tfidf_weight,word)



