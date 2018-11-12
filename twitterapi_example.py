# hashtagtimeseries.py
'''A simple demonstration of the twitter API'''
#
from TwitterAPI import TwitterAPI
#import HashTagMiner
#import matplotlib.pyplot as plt
#import pandas as pd

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

r = api.request('statuses/user_timeline', {'screen_name':'neilcghart','count':5})
for i,item in enumerate(r.get_iterator()):
    if 'text' in item:
        print(i,item['text'])
        print ("------------------")

r = api.request('search/tweets', {'q':'remembrance','count':100})
latlon = []
location= []
cnt=0
for item in r:
    if item['user']['location'] != '':
        location.append(item['user']['location'])
    if item['geo'] != None:
        latlon.append(item['geo'])
    cnt+=1
print('%d of %d tweets had geolocations' %(len(latlon),cnt))
print('%d of %d tweets had named locations' %(len(location),cnt))
