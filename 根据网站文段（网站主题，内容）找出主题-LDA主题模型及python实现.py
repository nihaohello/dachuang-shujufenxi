#coding=utf-8
import re
import jieba
import jieba.analyse  # 提取关键内容
import jieba.posseg as pseg  # 词性标注
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
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


list0 = []
#去除停用词
list0 = del_stop_words(cut_words(listall),stopwords)
listall1 = list(set(list0))
listall1.sort(key = list0.index)
comment_list=listall1
# print(listall1)


vectorizer = CountVectorizer()
# cntVector = CountVectorizer(stop_words=stopwords)
# transformer = TfidfTransformer()
# tfidf = transformer.fit_transform(vectorizer.fit_transform(listall1))
cntTf = vectorizer.fit_transform(comment_list)
terms = vectorizer.get_feature_names()
# print(terms)  #词量
# print("词频向量:")
# print(cntTf)
# 主题数量
n_topics=1
lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
docres = lda.fit_transform(cntTf)

# 通过fit_transform函数，我们就可以得到文档的主题模型分布在docres中。而主题词分布则在lda.components_中。

# print(docres)#
# print(lda.components_)
top_num=5
for topic_idx,topic in enumerate(lda.components_):
    # print(topic_idx)
    # print(topic)
    print("topic %d:" % topic_idx)
    print(topic.argsort())
    num=[]
    # for i in topic.argsort()[:-top_num - 1:-1]:
    for i in topic.argsort()[1:top_num]:
        num.append(i)
    for i in num:
        print(terms[i])
    # print(" ".join([terms[i] for i in topic.argsort()[:-top_num-1:-1]]))


