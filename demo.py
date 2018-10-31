import tweepy
from tweepy import Stream
from tweepy.auth import OAuthHandler
from tweepy.streaming import StreamListener
import time
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import sys
import json
import webbrowser
from urllib.request import urlopen
from xlwt import Workbook
import xlrd
from urllib.request import urlopen
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def getplace(add):
    add=add.replace(" ","")
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyBBcAwe8bTVYXsdKXZlzyY6ST3q8bL4adE" %(add)
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    return country


wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

tweets=[]

consumer_key = 'OasHtQUm1FWXVeRl4mloCDCYy'
consumer_secret = 'raZDNQK2ItPLDMM6x0k1l0IjIyZT3pu1ZCu98UE2Uw8aAkhY8t'
access_token = '1609726374-j2Q4y6Jc6EBd0cORmObACgVZexpxG4maqnOVYxk'
access_secret = 'u0uXLIVaPTinKk1Z3HdhFDnTlUIB6aFTsDC9px1Kn17XL'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

#api = tweepy.API(auth)

c=0
sheet1.write(0, 0, 'S.No.')
sheet1.write(0, 1, 'User')
sheet1.write(0, 2, 'Location')
sheet1.write(0, 3, 'Time of creation')
sheet1.write(0, 4, 'Tweet')

class tweetlistener(StreamListener):
    def on_data(self, data):
        global c
        global s
        global tweets
        c=c+1
        all_data=json.loads(data)
        print(c)
        '''print("User - ", all_data["user"]["name"])
        print("User's screen - ", all_data["user"]["screen_name"])
        print("Tweet - ", all_data["text"])
        print("Source - ", all_data["source"])
        print("Location - ", all_data["user"]["location"])
        print("Source - ", all_data["created_at"])'''

        sheet1.write(c, 0, c)
        sheet1.write(c, 1, all_data["user"]["name"])
        sheet1.write(c, 2, all_data["user"]["location"])
        sheet1.write(c, 3, all_data["created_at"])
        sheet1.write(c, 4, all_data["text"])

        tweets.append(all_data["text"])

        if(c==count):
            name=s+".xls"
            wb.save(name)
            return(False)
        else:
            #time.sleep(2)
            return(True)


    def on_error(self, status):
        print(status)


s=input("Enter search keyword - ")
count=int(input("Enter Number of tweets to be analyzed - "))
query="https://twitter.com/search?q="+s
webbrowser.open_new(query)
twitterStream = Stream(auth, tweetlistener())
twitterStream.filter(track=[s],languages=["en"])
print()

loc = (s+".xls")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)


country=[]
for i in range(1,count+1):
   if(sheet.cell_value(i,2)!=""):
        try:
           country.append(getplace(sheet.cell_value(i,2)))
        except:
            s=0

x=set(country)

print(len(country),len(x))
y=[]

for i in x:
    y.append(country.count(i))

x_pos = np.arange(len(x))
plt.bar(x_pos, y, align='center', alpha=0.5)
plt.xticks(x_pos, x)
plt.ylabel('Count')
plt.title('Tweets')
plt.savefig("fig.png")


tweet = ' '
stopwords = set(STOPWORDS)
for val in tweets:
    val = str(val)
    tokens = val.split()
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    for words in tokens:
        tweet = tweet + words + ' '

wordcloud = WordCloud(width=600, height=600,background_color='black',stopwords=stopwords,min_font_size=10).generate(tweet)

# plot the WordCloud image
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()