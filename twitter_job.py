from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "16226678-frJAvZX1hkcOIrBAKs7Vmem5vx4XDYUdVXzABRCQC"
access_token_secret = "f8Zh0eyuJB49RJi5aO5EB1uYLpaOIxU3GQ4ULULGh7A5H"
consumer_key = "uTqsqrmUqckfSDyBvK4H9K8m2"
consumer_secret = "ZFE9PVxsE1wmPEJvrqKjRpvLAutMhejfXL49ny2fiNqsiEgSrs"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'jobs', 'unemployed', 'pink slip'
    stream.filter(track=['jobs', 'unemployed', 'pink slip'])