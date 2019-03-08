import tweepy

from credentials import *

def get_recent_tweets(api, screen_name):

  tweets = api.user_timeline(screen_name = screen_name,count=50)
  
  outtweets = ""
  tweetids = ""

  for tweet in tweets:
    outtweets = outtweets + " " + tweet.text.encode('utf-8')
    tweetids = tweetids + "\n" + str(tweet.id)
  
  with open(screen_name+'s_tweets.txt', 'a') as f:
      f.write(outtweets)
      
  with open(screen_name+'_tweetids.txt', 'a') as f:
      f.write(tweetids)

if __name__ == '__main__':
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  api = tweepy.API(auth)

