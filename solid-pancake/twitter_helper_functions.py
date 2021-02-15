import twitter 
from dotenv import load_dotenv #used to load api keys via env file
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import string
from nltk.corpus import stopwords
stopwords.words('english')

def get_tweets(api=None, screen_name=None):
    """Gets the timeline/tweets for the provided user's screen_name. It overcomes
    the 200 tweet limit by re-running a while loop until the earliest tweet is
    found from the timeline.

    Args:
        api (twitterAPIObject, optional): Provide the initialized twtitter API
        object. Defaults to None.
        screen_name (string, optional): Twitter screen name of user to find 
        tweets of. Must include @ at the beginning. Defaults to None.

    Returns:
        [type]: [description]
    """
    
    timeline = api.GetUserTimeline(screen_name=screen_name,
                                   count=200,
                                   exlude_replies=True,
                                   include_rts=False)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("Getting tweets before: ", earliest_tweet)
    
    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, 
            count=200, 
            exclude_replies=True, 
            include_rts=False
        )
        new_earliest = min(tweets, key = lambda x: x.id).id
        
        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("Getting tweets before: ", earliest_tweet)
            timeline += tweets
        
    return timeline

def convert_tweets_to_list(timeline):
    """Converts a list tweet objects into string object for easier parsing 
    in downstream algorithms.

    Args:
        timeline ([tweet]): list of tweets

    Returns:
        [string]: list of tweets converted into string
    """
    list_tweets = []
    for tweet in timeline:
        list_tweets.append(tweet.text)
        
    return list_tweets

def generate_word_cloud(list_tweets, stopwords=None):
    """Generates a wordcloud for the given list of strings.

    Args:
        list_tweets ([string]): list of tweets as strings
        stopwords ([STOPWORDS], optional): Provide stop words to be removed from
        list of strings before generating the word cloud. Defaults to None.

    Returns:
        [WordCloud]: A WordCloud instance that can be used with plt.imshow()
    """
    tweets_joined = " ".join(list_tweets)
    
    return WordCloud(stopwords=stopwords).generate(
        tweets_joined
    )
    
def message_cleaning_pipeline(message):
    """Cleans a given message by removing punctuations and stop words, and 
    lowercasing the words inside.

    Args:
        sentence (string): message to be cleaned

    Returns:
        [string]: list of words in the message after processing
    """
    sent_without_punc = [char for char in message if char not in string.punctuation]
    sent_without_punc = ''.join(sent_without_punc)
    sent_without_punc_clean = [word for word in sent_without_punc.split() if word.lower() not in stopwords.words('english')]
    return sent_without_punc_clean
    
