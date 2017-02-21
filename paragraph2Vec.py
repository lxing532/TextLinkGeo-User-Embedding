from gensim.models import doc2vec
from collections import namedtuple,Counter
import re
import string
import random
import numpy as np
from numpy import linalg as la
import tweepy

def auth_api():
    key_tokens = {}

    key_tokens['consumer_key'] = ''
    key_tokens['consumer_secret'] = ''
    key_tokens['access_token'] = ''
    key_tokens['access_secret'] = ''

    auth_twitter = tweepy.OAuthHandler(key_tokens['consumer_key'],key_tokens['consumer_secret'])
    auth_twitter.set_access_token(key_tokens['access_token'],key_tokens['access_secret'])
    api_twitter = tweepy.API(auth_twitter)

    return api_twitter
#implement para2vec with gensim
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

#euclid similarity
def euclidSimilar(inA,inB):
    return 1.0/(1.0+la.norm(inA-inB))

#cosin similarity
def cosSimilar(inA,inB):
    inA=np.mat(inA)
    inB=np.mat(inB)
    num=float(inA*inB.T)
    denom=la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)


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
    LabelDoc = namedtuple('LabelDoc','words tags')
    exclude = set(string.punctuation)
    #exclude.remove('@')        #?
    #exclude.remove('#')        #?
    #exclude.remove('_')
    #exclude.remove('-')
    #exclude.remove('&')

    all_docs = []
    count = 0
    for sen in data_list:
        word_list = sen.split()
        tag = ['SEN_'+str(count)]
        count += 1
        sen = ''.join(ch for ch in sen if ch not in exclude)
        all_docs.append(LabelDoc(sen.split(),tag))
    print(len(userList),len(data_list))

    return all_docs, userList


def addRelation(all_docs,userList):

    nameDict = {}
    holder = ''
    for line in open(''):
        line = line.strip()
        s = ''
        if line != '' and line[-1] == ':':
            for ch in line:
                if ch == ' ':
                    holder = s
                    break
                s += ch
            nameDict[holder] = []
        else:
            pre = ''
            ss = ''
            for ch in line:
                if pre == '|':
                    if ch == '|':
                        ss = ss[2:]
                        ss = ss[:-2]
                        nameDict[holder].append(ss)
                        break
                    ss += ch
                else:
                    pre = ch
    keyList = list(nameDict.keys())
    for i in range(len(userList)):
        if userList[i] in keyList:
            l = nameDict[userList[i]]
            all_docs[i].words.append('USR')
            for name in l:
                all_docs[i].words.append('USR')
                all_docs[i].words.append(name)
                all_docs[i].words.append('USR')
            all_docs[i].words.append('USR')
    return all_docs

if __name__ == '__main__':
    api_twitter = auth_api()
    all_docs, userList = content()
    newall_docs = addRelation(all_docs,userList)
    model = doc2vec.Doc2Vec(size=75, window=1, alpha=0.025,min_alpha=0.025, min_count=5)
    model.build_vocab(newall_docs)
    for epoch in range(10):
        model.train(newall_docs)
        model.alpha -= 0.002
        model.min_alpha = model.alpha

    model.save('model.doc2vec')
    precision = []
    recall = []
    MMR = []
######################################################################
    friendDict = {}
    hold = ''
    for line in open(''):
        if ':' in line:
            l = line.strip()
            hold = l[:-1]
        else:
            friendDict[hold] = line.strip().split(' ')
    print(len(friendDict))


    indexList = [875, 681, 805, 922, 115, 320, 907, 317, 853, 773, 917, 894, 935, 1038, 57, 332, 96, 146, 258, 299, 841, 579, 453, 494, 357, 438, 165, 687, 848, 851, 602, 364, 1003, 562, 551, 556, 874, 88, 175, 464, 336, 231, 767, 39, 114, 550, 830, 187, 654, 852, 912, 281, 552, 203, 20, 47, 206, 293, 783, 385, 95, 680]
    for i in indexList:
        mmr = 0
        doc_id = i
        count = 0
        c = 0
        sims = model.docvecs.most_similar(doc_id, topn=model.docvecs.count)
        print('TARGET' , newall_docs[doc_id].words)
        candident = []
        resList = []
        for j in sims:
            if count == 60:
                break
            #pid = int(string.replace(i[0], "SEN_", ""))
            #print(i[0],": ", all_docs[pid].words)
            num = j[0]
            numeric = int(num[4:])
            print(j[0],userList[numeric])
            candident.append(userList[numeric])
            count += 1
        trueList = friendDict[userList[i]]
        print(userList[i])
        order = 0
        for k in candident:
            order += 1
            if k in trueList:
                c += 1
                print(count)
                mmr += float(1)/order
        tp = float(c)/60
        re = float(c)/len(trueList)
        precision.append(tp)
        recall.append(re)
        if c != 0:
            MMR.append(mmr/c)
            print(mmr,c)
            print(mmr/c)
        print(tp)
        print(re)
    print(sum(precision)/62)
    print(sum(recall)/62)
    print(sum(MMR)/62)






