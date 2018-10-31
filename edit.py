import time
from tweepy import Stream
from tweepy.auth import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
import nltk


def calctime(a):
    return time.time() - a


positive = 0
negative = 0
compound = 0

count = 0
initime = time.time()
plt.ion()

import test

ckey = 'OasHtQUm1FWXVeRl4mloCDCYy'
csecret = 'raZDNQK2ItPLDMM6x0k1l0IjIyZT3pu1ZCu98UE2Uw8aAkhY8t'
atoken = '1609726374-j2Q4y6Jc6EBd0cORmObACgVZexpxG4maqnOVYxk'
asecret = 'u0uXLIVaPTinKk1Z3HdhFDnTlUIB6aFTsDC9px1Kn17XL'


class listener(StreamListener):

    def on_data(self, data):
        global initime
        t = int(calctime(initime))
        all_data = json.loads(data)
        tweet = all_data["text"].encode("utf-8")
        # username=all_data["user"]["screen_name"]
        tweet = " ".join(re.findall("[a-zA-Z]+", tweet.decode('utf-8')))
        blob = TextBlob(tweet.strip())

        global positive
        global negative
        global compound
        global count

        count = count + 1
        senti = 0
        positive=0
        negative=0
        for sen in blob.sentences:
            senti = senti + sen.sentiment.polarity
            if sen.sentiment.polarity >= 0:
                positive = sen.sentiment.polarity
            else:
                negative = sen.sentiment.polarity
        compound = compound + senti
        print("~~~  NEW TWEET   ~~~")
        print(count)
        print("User - ", all_data["user"]["name"])
        print("User's screen - ", all_data["user"]["screen_name"])
        print("Tweet - ", tweet.strip())
        print("Source - ", all_data["source"])
        print("Location - ", all_data["user"]["location"])
        print("Source - ", all_data["created_at"])
        print(senti)
        #print(compound)
        #print(t)
        print(str(positive) + ' ' + str(negative) + ' ' + str(compound))
        print()

        if(positive!=0.0 or negative!=0.0):
            plt.axis([0, 120, -4, 4])
            plt.xlabel('Time')
            plt.ylabel('Sentiment')
            plt.plot([t], [positive], 'go', [t], [negative], 'ro')
            #plt.plot([t], [positive], 'go', [t], [negative], 'ro', [t], [compound], 'bo')
            plt.show()
            plt.pause(0.0001)
            if count == 200:
                return False
            else:
                return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener(count))
twitterStream.filter(track=[input("Enter Keyword - ")])