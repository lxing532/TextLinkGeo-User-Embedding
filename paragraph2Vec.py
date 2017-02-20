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


def relation():
    LabelDoc = namedtuple('LabelDoc','words tags')
    f1 = ['1','12','22','45','668','324','556','1208','1111019','32423840','42423525']
    f2 = ['1111019','1208','42423525','40414729','401840','401984','480180198','83018','13890918']
    f3 = ['1','45','924701924','41098','849018','8301','840184','72981','8019','89742374','74759']
    f4 = ['1','8301','72981','94810','7412940','20793','32090820','719','7427974']
    big = []
    big.append(f1)
    big.append(f2)
    big.append(f3)
    big.append(f4)
    all_docs = []
    for i in range(4):
        tag = ['SEN_'+str(i)]
        all_docs.append(LabelDoc(big[i],tag))
    return all_docs

if __name__ == '__main__':
    api_twitter = auth_api()
    all_docs, userList = content()
    model = doc2vec.Doc2Vec(size=75, window=1, alpha=0.025,min_alpha=0.025, min_count=5)
    model.build_vocab(all_docs)
    for epoch in range(10):
        model.train(all_docs)
        model.alpha -= 0.002
        model.min_alpha = model.alpha

    model.save('model.doc2vec')
    precision = []
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


    indexList = [877, 683, 807, 924, 115, 321, 909, 318, 855, 775, 919, 896, 938, 1041, 57, 333, 96, 146, 259, 300, 843, 581, 455, 496, 358, 440, 166, 689, 850, 853, 604, 365, 1006, 564, 553, 558, 876, 88, 176, 466, 337, 232, 769, 39, 114, 552, 832, 188, 656, 854, 914, 282, 554, 204, 20, 47, 207, 294, 785, 386, 95, 682]
    for i in indexList:
        mmr = 0
        doc_id = i
        count = 0
        c = 0
        sims = model.docvecs.most_similar(doc_id, topn=model.docvecs.count)
        print('TARGET' , all_docs[doc_id].words)
        candident = []
        resList = []
        for j in sims:
            if count == 10:
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
        tp = float(c)/10
        precision.append(tp)
        if c != 0:
            MMR.append(mmr/c)
            print(mmr,c)
            print(mmr/c)
        print(tp)
    print(sum(precision)/62)
    print(sum(MMR)/62)
######################################################################
 


