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

def addLocation(all_docs,userList):

    stateDict =  {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming',
        'AB': 'Alberta',
        'BC': 'British Columbia',
        'MB': 'Manitoba',
        'NB': 'New Brunswick',
        'NL': 'Newfoundland and Labrador',
        'NT': 'Northwest Territories',
        'NS': 'Nova Scotia',
        'NU': 'Nunavut',
        'ON': 'Ontario',
        'PE': 'Prince Edward Island',
        'QC': 'Quebec',
        'SK': 'Saskatchewan',
        'YT': 'Yukon'
    }
    state2timezone = { 'AK': 'Alaska', 'AL': 'Central', 'AR': 'Central', 'AS': 'Samoa', 'AZ': 'Mountain', 'CA': 'Pacific', 'CO': 'Mountain', 'CT': 'Eastern', 'DC': 'Eastern', 'DE': 'Eastern', 'FL': 'Eastern', 'GA': 'Eastern', 'GU': 'Pacific', 'HI': 'Hawaii', 'IA': 'Central', 'ID': 'Mountain', 'IL': 'Central', 'IN': 'Eastern', 'KS': 'Central', 'KY': 'Eastern', 'LA': 'Central', 'MA': 'Eastern', 'MD': 'Eastern', 'ME': 'Eastern', 'MI': 'Eastern', 'MN': 'Central', 'MO': 'Central', 'MP': 'Pacific', 'MS': 'Central', 'MT': 'Mountain', 'NC': 'Eastern', 'ND': 'Central', 'NE': 'Central', 'NH': 'Eastern', 'NJ': 'Eastern', 'NM': 'Mountain', 'NV': 'Pacific', 'NY': 'Eastern', 'OH': 'Eastern', 'OK': 'Central', 'OR': 'Pacific', 'PA': 'Eastern', 'PR': 'America', 'RI': 'Eastern', 'SC': 'Eastern', 'SD': 'Central', 'TN': 'Central', 'TX': 'Central', 'UT': 'Mountain', 'VA': 'Eastern', 'VI': 'America', 'VT': 'Eastern', 'WA': 'Pacific', 'WI': 'Central', 'WV': 'Eastern', 'WY': 'Mountain'}
    state2region = { 'AK': 'west', 'AL': 'South', 'AR': 'South', 'AS': 'Samoa', 'AZ': 'southwest', 'CA': 'west', 'CO': 'west', 'CT': 'New-England', 'DC': 'Mid-Atlantic', 'DE': 'Mid-Atlantic', 'FL': 'South', 'GA': 'South', 'GU': 'Pacific', 'HI': 'west', 'IA': 'Midwest', 'ID': 'west', 'IL': 'Midwest', 'IN': 'Midwest', 'KS': 'Midwest', 'KY': 'South', 'LA': 'South', 'MA': 'New-England', 'MD': 'Mid-Atlantic', 'ME': 'New-England', 'MI': 'Midwest', 'MN': 'Midwest', 'MO': 'Midwest', 'MP': 'Pacific', 'MS': 'South', 'MT': 'west', 'NC': 'South', 'ND': 'Midwest', 'NE': 'Midwest', 'NH': 'New-England', 'NJ': 'Mid-Atlantic', 'NM': 'southwest', 'NV': 'west', 'NY': 'Mid-Atlantic', 'OH': 'Midwest', 'OK': 'southwest', 'OR': 'west', 'PA': 'Mid-Atlantic', 'PR': 'America', 'RI': 'New-England', 'SC': 'South', 'SD': 'Midwest', 'TN': 'South', 'TX': 'southwest', 'UT': 'west', 'VA': 'South', 'VI': 'America', 'VT': 'New-England', 'WA': 'west', 'WI': 'Midwest', 'WV': 'South', 'WY': 'west'}

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
            l = line.strip().split('  |  ')
            if len(l) == 3:
                if ',' in l[2] and ':' not in l[2][:-1]:
                    l[2] = l[2].strip()
                    for k,v in stateDict.items():
                        if k in l[2] or v in l[2]:
                            if v in l[2]:
                                old = v
                                new = k
                                tmp = l[2]
                                l[2] = tmp.replace(old,new)
                            nameDict[holder].append(l[2])

    keyList = list(nameDict.keys())
    for i in range(len(userList)):
        if userList[i] in keyList:
            l = nameDict[userList[i]]
            all_docs[i].words.append('LOC')
            for name in l:
                l2 = name.strip().split(', ')
                all_docs[i].words.append('LOC')
                #for k,v in state2region.items():
                    #if k in name:
                        #all_docs[i].words.append(v)
                for loc in range(len(l2)):
                    all_docs[i].words.append(l2[loc])
                all_docs[i].words.append('LOC')
            all_docs[i].words.append('LOC')
    return all_docs

if __name__ == '__main__':
    api_twitter = auth_api()
    all_docs, userList = content()
    print(userList.index("19730865"),userList.index("14724725"),userList.index("77235516"),userList.index("44988185"))
    newall_docs = addRelation(all_docs,userList)
    nnewall_docs = addLocation(newall_docs,userList)
    model = doc2vec.Doc2Vec(size=75, window=1, alpha=0.025,min_alpha=0.025, min_count=5)
    model.build_vocab(nnewall_docs)
    for epoch in range(10):
        model.train(nnewall_docs)
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
    reDict = {}
    #indexList = [875, 681, 805, 922, 115, 320, 907, 317, 853, 773, 917, 894, 935, 1038, 57, 332, 96, 146, 258, 299, 841, 579, 453, 494, 357, 438, 165, 687, 848, 851, 602, 364, 1003, 562, 551, 556, 874, 88, 175, 464, 336, 231, 767, 39, 114, 550, 830, 187, 654, 852, 912, 281, 552, 203, 20, 47, 206, 293, 783, 385, 95, 680]
    #indexList = [875, 681, 922, 115, 320, 907, 317, 853, 773, 917, 894, 1038, 57, 332, 146, 258, 299, 841, 579, 453, 494, 357, 438, 165, 687, 848, 602, 364, 1003, 562, 551, 556, 874, 88, 175, 464, 336, 231, 767, 39, 114, 550, 830, 187, 654, 852, 912, 281, 552, 203, 20, 47, 206, 293, 783, 385, 95, 680]
    indexList = [681, 805, 922, 115, 320, 907, 317, 853, 773, 917, 894, 935, 1038, 57, 332, 96, 146, 258, 299, 841, 579, 453, 494, 357, 438, 165, 687, 848, 851, 602, 364, 1003, 562, 551, 556, 874, 88, 175, 464, 336, 231, 767, 39, 114, 550, 830, 187, 654, 912, 281, 552, 203, 20, 47, 206, 293, 783, 680]

    for i in indexList:
        mmr = 0
        doc_id = i
        count = 0
        c = 0
        sims = model.docvecs.most_similar(doc_id, topn=model.docvecs.count)
        print('TARGET' , nnewall_docs[doc_id].words)
        candident = []
        resList = []
        for j in sims:
            if count == 40:
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
        tp = float(c)/40
        re = float(c)/len(trueList)
        precision.append(tp)
        recall.append(re)
        if c != 0:
            MMR.append(mmr/c)
            print(mmr,c)
            print(mmr/c)
        print(tp)
        print(re)
        reDict[userList[i]] = c
    print(sum(precision)/58)
    print(sum(recall)/58)
    print(sum(MMR)/58)
    print(sorted(reDict.items(), key=lambda d: d[1]))







