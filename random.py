import re
import string
import random
from copy import deepcopy
def content():
    data_list = []
    userList = []
    c = 0
    holder = ''
    user_str = ''
    for line in open('/users/xinglinzi/desktop/ISdata/Tweetsss(2500).txt'):
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

def user2Uni():
    D = {}
    l1 = [];l2 = []
    for line in open('/Users/xinglinzi/desktop/pickedFollowers(2500).txt'):

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

if __name__ == '__main__':

     all_doc, userList = content()
     friendDict = {}
     hold = ''
     for line in open('/users/xinglinzi/desktop/ISdata/TestObj.txt'):
        if ':' in line:
            l = line.strip()
            hold = l[:-1]
        else:
            friendDict[hold] = line.strip().split(' ')

     indexList = [877, 683, 807, 924, 115, 321, 909, 318, 855, 775, 919, 896, 938, 1041, 57, 333, 96, 146, 259, 300, 843, 581, 455, 496, 358, 440, 166, 689, 850, 853, 604, 365, 1006, 564, 553, 558, 876, 88, 176, 466, 337, 232, 769, 39, 114, 552, 832, 188, 656, 854, 914, 282, 554, 204, 20, 47, 207, 294, 785, 386, 95, 682]

     precision = []; MMR = []
     choseNum = 50
     for i in indexList:

        p = 0
        mmr = 0
        allc = 0
        user = userList[i]
        trueList = friendDict[user]
        tmpList = deepcopy(userList)
        tmpList.remove(userList[i])
        choseList = random.sample(tmpList,50)

        for j in choseList:
            allc += 1
            if j in trueList:
                p += 1
                mmr += float(1)/allc

        precision.append(float(p)/choseNum)
        if p != 0:
            MMR.append(mmr/p)

     print(sum(precision)/62)
     print(sum(MMR)/62)