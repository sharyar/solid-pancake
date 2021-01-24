from os import times
import os
from typing import Counter
import dotenv
import twitter
import json
import sys
from dotenv import load_dotenv


def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, 
                                   count=200, 
                                   exclude_replies=True, 
                                   include_rts=False)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, 
            count=200, 
            exclude_replies=True, 
            include_rts=False
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline

if __name__ == '__main__':
    
    # This loads the .env file that stores API and CONSUMER KEYS.
    # Avoids having them exposed via github. 
    load_dotenv()
    
    try: 
        CONSUMER_KEY = os.getenv('CONSUMER_KEY')
        CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
        ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
        ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    except Exception as e:
        print('This exception occured', e)
    
    else:
        api = twitter.Api(consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN_KEY,
                    access_token_secret=ACCESS_TOKEN_SECRET)
        
        screen_name = sys.argv[1]
        print(screen_name)
        timeline = get_tweets(api=api, screen_name=screen_name)
        
        for tweet in timeline:
            print(tweet.text)
            break
        
        with open('timeline.json', 'w+') as f:
            for tweet in timeline:
                f.write(json.dumps(tweet._json))
                f.write('\n')