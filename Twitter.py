import concurrent.futures
import random
import time
import tweepy
import twitter
from datetime import datetime

class TweetModule:

    def set_api(self):
        self.api = twitter.Api(consumer_key='ej9xM4fp6CXo9jxbn8HSfuaMX',
                          consumer_secret='p1zqluAO67dSrpDHDDFAw6mZTxWTQy6acyWAShulaA07etIN3H',
                          access_token_key='4165914892-Stzhsbf10jyoZBsylN7PurQTNGYh2K9WsdFRgOI',
                          access_token_secret='SuBmCVz3csEqNp9fanOhi3mopfC2gBycghNr1yxwaGI7R')

    def __init__(self,users):
        self.users = users
        self.set_api()
        self.retrieve_tweets()

    def retrieve_tweets(self):
        self.retrieved_tweets = []
        for user in self.users:
            print('User:',user)
            tweets = self.api.GetUserTimeline(screen_name=user,count=200)
            for tweet in tweets:
                print(tweet)
                self.retrieved_tweets.append(tweet)

class TweepyModule:

    def set_api(self):
        self.auth = tweepy.AppAuthHandler("ej9xM4fp6CXo9jxbn8HSfuaMX", "p1zqluAO67dSrpDHDDFAw6mZTxWTQy6acyWAShulaA07etIN3H")
        self.api = tweepy.API(self.auth)
        self.api_twitter_official = twitter.Api(consumer_key='ej9xM4fp6CXo9jxbn8HSfuaMX',
                               consumer_secret='p1zqluAO67dSrpDHDDFAw6mZTxWTQy6acyWAShulaA07etIN3H',
                               access_token_key='4165914892-Stzhsbf10jyoZBsylN7PurQTNGYh2K9WsdFRgOI',
                               access_token_secret='SuBmCVz3csEqNp9fanOhi3mopfC2gBycghNr1yxwaGI7R')

    def get_ID(self):
        self.user_id = {}
        for user in self.users:
            self.user_id[user] = self.api_twitter_official.UsersLookup(screen_name=user)[0].AsDict()['id']

    def __init__(self,users,start,end):
        self.users = users
        self.start = start
        self.end = end
        self.set_api()
        self.get_ID()
        self.current_handle_index = 0
        self.all_tweets = {}
        self.run_tweet_getter()
        print('Tweets have be downloaded')

    def run_tweet_getter(self):
        future = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for user in self.users:
                print(user)
                future[user] = executor.submit(self.get_tweets,handle=user)
            for user in self.users:
                self.all_tweets[user] = future[user].result()

    def retrieve_tweets(self):
        self.retrieved_tweets = []
        index = 0
        for user in self.users:
            tweets = self.api.user_timeline(screen_name = user,count=200)
            tweet0 = None
            for tweet in tweets:
                if tweet0 == None:
                    tweet0 = tweet
                print(tweet.created_at)
                index += 1
        print(index)

    def to_datetime(self,a):
        return datetime.fromtimestamp(a)

    def get_tweets(self, handle):
        #print(handle)
        time.sleep(random.randrange(0,10)/2)
        start_day = self.start
        end_day = self.end
        start_day = self.to_datetime(start_day)
        end_day = self.to_datetime(end_day)
        total_tweets = 0
        times_slept = 0
        user_tweets = []
        tweet_count = 0
        user_id = self.user_id[handle]
        prev_tweet_time = None
        earliest_tweet_id = None
        while True:
            try:
                if earliest_tweet_id == None: # Runs on first go
                    timeline = self.api.user_timeline(id=user_id, count=200)
                else:
                    timeline = self.api.user_timeline(id=user_id,max_id=earliest_tweet_id)
            except Exception as e:
                if e.response.status == 429:
                    #print('sleeping')
                    times_slept += 1
                    if times_slept == 2:
                        break
                    time.sleep(60)
                    times_slept = 0
                else:
                    foo = None
                    #print('Could not access twitter ID:',user_id)
            found_early_tweets = False
            for tweet in timeline:
                if tweet.created_at >= start_day:
                    if prev_tweet_time == tweet.created_at:
                        #print('broke')
                        tweet_count += 1
                        if tweet_count == 3:
                            time.sleep(0.5)
                        else:
                            continue
                    total_tweets += 1
                    user_tweets.append(tweet)
                    prev_tweet_time = tweet.created_at
                else:
                    found_early_tweets = True
                if earliest_tweet_id == None or tweet.id < earliest_tweet_id:
                    earliest_tweet_id = tweet.id
                #print(total_tweets)
            if found_early_tweets:
                return user_tweets
        return user_tweets







