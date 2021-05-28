from wordcloud import WordCloud
from wordcloud import STOPWORDS as stp
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
from joblib import dump, load
import numpy as np
import base64
from io import BytesIO

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Some of the functions are based on coursera project:
# https://www.coursera.org/learn/twitter-sentiment-analysis/home/welcome

VECTORIZER_FILE = 'count_vectorizer.pickle'
NB_MODEL_FILE = 'nb_twitter_model.joblib'


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
                                   exclude_replies=True,
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
        new_earliest = min(tweets, key=lambda x: x.id).id

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
    """Generates a WordCloud for the given list of strings.

    Args:
        list_tweets ([string]): list of tweets as strings
        stopwords ([STOPWORDS], optional): Provide stop words to be removed from
        list of strings before generating the word cloud. Defaults to None.

    Returns:
        [WordCloud]: A WordCloud instance that can be used with plt.imshow()
    """
    tweets_joined = " ".join(list_tweets)

    plt.imshow(WordCloud(stopwords=stopwords).generate(
        tweets_joined
    ))
    plt.show()


def message_cleaning_pipeline(message):
    """Cleans a given message by removing punctuations and stop words, and 
    lower-casing words inside.

    Args:
        message (string): message to be cleaned

    Returns:
        [string]: list of words in the message after processing
    """

    # Remove punctuations
    sent_without_punc = [char for char in message if char not in string.punctuation]
    # Combine into a single string
    sent_without_punc = ''.join(sent_without_punc)
    # Remove stop words from string
    sent_without_punc_clean = [word for word in sent_without_punc.split() if
                               word.lower() not in stopwords.words('english')]

    return sent_without_punc_clean


def vectorize_tweets(tweets, analyzer=message_cleaning_pipeline, load_fitted_vectorizer=True):
    """Converts a given list of tweets in to their vectorized forms by using
    scikit-learn's text CountVectorizer. By default, the function will try
    to load a saved fitted vectorizer. This is required to ensure consistent 
    count vectorization across the training data and new data. It also does the 
    tweet cleaning by using the passed in analyzer function. 

    Args:
        tweets ([string]): list of tweets as strings
        analyzer ([function], optional): Provide a message cleaning function. 
        Defaults to message_cleaning_pipeline.
        load_fitted_vectorizer (bool, optional): Specifies if a pre-save model
        should be loaded for the vectorizer. This should be the case when analyzing
        new tweets but set to false when training the model. This will save the
        model to disk to be pre-loaded on a subsequent run. Defaults to True.

    Returns:
        np.array: returns a np array of vectorize tweets. It will have the shape
        (number_of_tweets, number_of_vectorized_words)
    """
    if load_fitted_vectorizer:
        try:
            with open(VECTORIZER_FILE, 'rb') as f:
                vectorizer = pickle.load(f)
        except FileNotFoundError as e:
            print(e)
        else:
            return vectorizer.transform(tweets)

    else:
        vectorizer = CountVectorizer(analyzer=message_cleaning_pipeline, dtype='uint8')
        vectorized_tweets = vectorizer.fit_transform(tweets)
        with open(VECTORIZER_FILE, 'wb+') as f:
            pickle.dump(vectorizer, f, pickle.HIGHEST_PROTOCOL)

        return vectorized_tweets


def train_and_save_model(tweets_x, labels):
    """
    Trains and saves a gaussian naive bayes classifier model based on pre-set paths. The model is saved to disk.
    It can be preloaded by using load_model function.
    Args:
        tweets_x: array of tweets to be used for training the classifier
        labels: array of labels for tweets

    Returns:
        nb_classifier: an instance of the trained gaussian model
    """
    vectorized_tweets = vectorize_tweets(tweets_x, analyzer=message_cleaning_pipeline, load_fitted_vectorizer=False)
    nb_classifier = MultinomialNB()
    nb_classifier.fit(vectorized_tweets, labels)
    # Save model:
    dump(nb_classifier, NB_MODEL_FILE)
    return nb_classifier


def load_model():
    """
    Loads a saved pre-trained classifier model from disk and returns it.
    Returns:
        nb_classifier: trained classifier model
    """
    nb_classifier = load(NB_MODEL_FILE)
    return nb_classifier


def analyze_and_visualize_tweets(tweets, nlp_model):
    # Run model on tweets. Return the array with counts of positive/negative labels
    # Vectorize tweets
    # Run model
    # Visualize results
    vectorized_tweets = vectorize_tweets(tweets)
    labels = nlp_model.predict(vectorized_tweets)
    positive_tweets = np.count_nonzero(labels == 0)
    negative_tweets = np.count_nonzero(labels == 1)

    print(f'Total Tweets: {len(tweets)}\nPositive Tweets: {positive_tweets}\n\
Negative Tweets:{negative_tweets}')

    plt.pie(x=[positive_tweets,negative_tweets], labels=['Positive Tweets', 'Negative Tweets'], shadow=False,
            autopct='%1.1f%%', explode=(0, 0.1))
    plt.show()
    
def analyze_and_visualize_tweets_web(tweets, nlp_model):
    vectorized_tweets = vectorize_tweets(tweets)
    labels = nlp_model.predict(vectorized_tweets)
    positive_tweets = np.count_nonzero(labels == 0)
    negative_tweets = np.count_nonzero(labels == 1)

    # plt.pie(x=[positive_tweets,negative_tweets], labels=['Positive Tweets', 'Negative Tweets'], shadow=False,
    #         autopct='%1.1f%%', explode=(0, 0.1))
    
    plt.bar(x=['Positive Tweets', 'Negative Tweets'], height=[positive_tweets, negative_tweets], color=['royalblue', 'lightcoral'])
    
    for index, data in enumerate((positive_tweets, negative_tweets)):
        plt.text(x=index, y=data+1, s=f"{data}", fontdict=dict(fontsize=10))
    
    buffer = BytesIO()
    
    plt.savefig(buffer, format='png')
    
    response = base64.b64encode(buffer.getbuffer()).decode('ascii')
    
    # Returns a formatted string that can be used as an output to a webpage 
    # as an image source
    return f'data:image/png;base64,{response}'
   
    
    
def generate_wordcloud_web(tweet_list, username):
    'Returns a word cloud formatted more appropriately for a web page'
    tweets_joined = " ".join(tweet_list)

    wc = WordCloud(stopwords=stp).generate(tweets_joined)
    
    wc.to_file(f'static/images/{username}-wordcloud.png')
    
