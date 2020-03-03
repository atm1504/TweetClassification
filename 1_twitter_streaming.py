# Step 1: tweet collection #

import datetime
import time
import sys
import os
import pandas as pd
from threading import Timer

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API
access_token = "Access token"
access_token_secret = "Access token secret"
consumer_key = "Consumer key"
consumer_secret = "Consumer key secret"

folder = "tweets"

#This is a basic listener that just prints received tweets to stdout.
class OutputListener(StreamListener):
    def __init__(self):
        self.filename = ""

    def update_filename(self):
        now = datetime.datetime.now()
        self.filename = now.strftime('%Y%m%d_%H')+'.txt'
        print ('[%s]write file: %s' % ((now.strftime('%Y%m%d_%H%M%S'),self.filename)))

    def on_data(self, data):
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(os.path.join(folder, self.filename),'a') as tf:
            tf.write(data)
        return True

    def on_error(self, status):
        print (status)

def run_timer(listener):
    listener.update_filename()
    Timer(60, run_timer, [listener]).start()


def getKeyWords():
    dataset = pd.read_csv("keywords.csv", index_col='Keyword')
    words=dataset.Keywords
    words=dataset[dataset.columns[0]]
    keywords = words.tolist()
    return keywords

def main():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # #This handles Twitter authentication and the connection to Twitter Streaming API
    l = OutputListener()
    run_timer(l)
    stream = Stream(auth, l)
    keywords = getKeyWords()

    while True:
        try:
            #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
            stream.filter(
                track=keywords)
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print(e)

if __name__ == '__main__':
    main()
