from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd

#Variables that contains the user credentials to access Twitter API 
access_token = "Access token"
access_token_secret = "Access token secret"
consumer_key = "Consumer key"
consumer_secret = "Consumer key secret"
# keywords = []


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

def getKeyWords():
    dataset = pd.read_csv("keywords.csv", index_col='Keyword')
    words=dataset.Keywords
    words=dataset[dataset.columns[0]]
    keywords = words.tolist()
    return keywords
    # print(keywords)
    # print(type(['python', 'javascript', 'ruby']))



if __name__ == '__main__':

    keywords = getKeyWords()
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=keywords)
    
