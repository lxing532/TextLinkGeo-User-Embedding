import tweepy
import random
import time

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

if __name__ == '__main__':

    api_twitter = auth_api()

    friendDict = {}
    holder = ''
    c = 0
    for line in open(''):
        if ':' in line.strip():
            tmp = line.strip()
            tmp = tmp[:-1]
            holder = tmp
            friendDict[tmp] = []
        else:
            friendDict[holder].append(line.strip())

    extractDict = {}
    for k,v in friendDict.items():

        if len(v) <= 100:
            extractDict[k] = v
        else:
            chosenList = random.sample(v,100)
            extractDict[k] = chosenList

    f = open('','w+')

    count = 1

    for k,v in extractDict.items():
        print('***********'+k+' '+str(c)+'************')
        c += 1
        try:
            user = api_twitter.get_user(user_id = int(k))
            screen_name = user.screen_name
            location = user.location
            if screen_name == '':
                screen_name = 'UUknowUU'
            if location == '':
                location = 'UUknowUU'
            f.write(k+'  |  '+screen_name+'  |  '+location+':\n')
            count += 1
            if count%900 == 0:
                time.sleep(910)
        except tweepy.error.TweepError:
                print("Failed to run the command on that user:"+id+", Skipping...")
                count += 1
        for id in v:
            try:
                user = api_twitter.get_user(user_id = int(id))
                screen_name1 = user.screen_name
                location1 = user.location
                if screen_name1 == '':
                    screen_name1 = 'UUknowUU'
                if location1 == '':
                    location1 = 'UUknowUU'
                f.write(id+'  |  '+screen_name1+'  |  '+location1+'\n')
                count += 1
                if count%900 == 0:
                    time.sleep(910)
            except tweepy.error.TweepError:
                print("Failed to run the command on that user:"+id+", Skipping...")
                count += 1




