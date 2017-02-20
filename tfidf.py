from gensim import corpora, models, similarities
import logging
import re
import string
import numpy as np
import random
from collections import namedtuple,Counter
from numpy import linalg as la
import copy

def user2Uni():
    D = {}
    l1 = [];l2 = []
    for line in open(''):

        l = line.strip().split(' ')
        if len(l) == 1:
            l1.append(l[0])
        else:
            l2.append(l)

    for i in range(len(l2)):
        u = l1[i]
        for j in l2[i]:
            D[j] = []

    for i in range(len(l2)):
        u = l1[i]
        for j in l2[i]:
            D[j].append(l1[i])
    return D

def content():
    data_list = []
    userList = []
    c = 0
    holder = ''
    user_str = ''
    for line in open(''):
        if 'xlz1015ahmj0923' in line:
            c += 1
            #print(c)
            #print(user_str)
            uid = line[15:]
            uid2 = uid[:-2]
            holder = uid2
            if user_str != '':
                data_list.append(user_str)
                user_str = ''
            continue

        if holder is not None:
            if line == '\n':
                continue
            else:
                userList.append(holder)
                holder = None
        if 'xlz1015ahmj0923' not in line:
            result = re.sub(r"http\S+", "", line.strip())
            result = re.sub(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])',"",result)
            result = re.sub('RT ','',result)
            user_str += ' '
            user_str += result
    data_list.append(user_str)

        #c += 1
        #if c == 5000:
            #break

    # separate long string into sentences based on '.?!'
    #sentenceEnders = re.compile('[.?!]')
    #data_list = sentenceEnders.split(data)
    #print(data_list)
    # eliminate sentence less than 3 words and all the punctuation
    #LabelDoc = namedtuple('LabelDoc','words tags')
    exclude = set(string.punctuation)
    exclude.remove('@')        #?
    exclude.remove('#')        #?
    exclude.remove('_')
    exclude.remove('-')
    exclude.remove('%')
    exclude.remove('$')
    exclude.remove('&')

    all_docs = []
    count = 0
    for sen in data_list:
        word_list = sen.split()
        tag = ['SEN_'+str(count)]
        count += 1
        sen = ''.join(ch for ch in sen if ch not in exclude)
        all_docs.append(sen.strip().split(' '))
    return all_docs, userList

if __name__ == '__main__':

    corp,userList = content()
    print(len(corp))
    dictionary = corpora.Dictionary(corp)
    corpus = [dictionary.doc2bow(text) for text in corp]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    friendDict = {}
    hold = ''
    for line in open(''):
        if ':' in line:
            l = line.strip()
            hold = l[:-1]
        else:
            friendDict[hold] = line.strip().split(' ')
    print(len(friendDict))

    precision = []
    indexList = [877, 683, 807, 924, 115, 321, 909, 318, 855, 775, 919, 896, 938, 1041, 57, 333, 96, 146, 259, 300, 843, 581, 455, 496, 358, 440, 166, 689, 850, 853, 604, 365, 1006, 564, 553, 558, 876, 88, 176, 466, 337, 232, 769, 39, 114, 552, 832, 188, 656, 854, 914, 282, 554, 204, 20, 47, 207, 294, 785, 386, 95, 682]
    for k in indexList:
        doc_id = k

        vec_bow = dictionary.doc2bow(corp[doc_id])
        vec_tfidf = tfidf[vec_bow]
        index = similarities.MatrixSimilarity(corpus_tfidf)
        sims = np.ndarray([])
        sims = index[vec_tfidf]
        similarity = list(sims)

        pro = [j for j in range(0,2043)]

        for i in range(len(similarity)-1):    # 这个循环负责设置冒泡排序进行的次数
            for j in range(len(similarity)-i-1):  # ｊ为列表下标
                if similarity[j] < similarity[j+1]:
                    similarity[j], similarity[j+1] = similarity[j+1], similarity[j]
                    pro[j], pro[j+1] = pro[j+1], pro[j]

        #print(similarity)
        #print(pro)

        #test = random.sample(pro, 50)
        print('TARGET' , corp[doc_id])
        count = 0
        trueList = friendDict[userList[k]]
        print(trueList)
        resList = []
        cc = 0
        for i in pro:
            if count == 40:
                break
            #pid = int(string.replace(i[0], "SEN_", ""))
            #print(i[0],": ", all_docs[pid].words)
            #num = i[0]
            #numeric = int(num[4:])
            print(i,userList[i])
            if userList[i] in trueList:
                cc += 1
                print(cc)
            count += 1
        tp = float(cc)/40
        print(tp)
        precision.append(tp)
    print(sum(precision)/62)

