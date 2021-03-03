# CLI application for sentiment analysis of a user's tweets

# Load constants
# Check if saved model exists, if it does not, ask user if ok to train
# Save model for vectorizer as well
# Get user's twitter address
# Ask if he wants a word cloud too
# Start analyzing - Show animation for loading? 

# display graph of sentiment analysis

# Import libraries needed:
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import time
import nltk
from nltk.corpus import stopwords
import twitter_helper_functions
from dotenv import load_dotenv
import twitter

nltk.download('stopwords')
stopwords.words('english')
# Constants:
TWITTER_DF_FILEPATH = '../twitter.csv'
# Declare variables used in the program

NLP_model = None
twitter_id = None
retrieved_tweets = None
twitter_api = None

WELCOME_MESSAGE = '''
Welcome to Solid-Pancake - A Twitter Sentiment Analysis Program
This is the command line version of the tool. A web-based version is
currently under development. 

By: Sharyar Memon

Please select from one of the following options:
1. Do sentiment analysis on your tweets!
2. Admin Access
3. Display Word Cloud
4. Run model on saved tweets! 
Q. Exit
'''

ADMIN_MESSAGE = '''
***************************
You are in the Admin Panel. Please select one of the following options:
1. Train Model from Default Dataset and save model
2. Specify New Dataset and Train - Must have a specific format (Check Docs)
3. Load saved-model!
Q. Go back to main menu. 
'''

USER_MESSAGE = f'''
***************************
You are in the USer Panel. Please select one of the following options:
1. Provide your twitter id: {twitter_id}
2. Generate Word Cloud from tweets
3. Do Sentiment Analysis and display a distribution of your tweet sentiments.
4. Admin Panel
Q. Quit Application
'''

EXIT_MESSAGE = '''
***************************
Thanks for trying my application! To reach out to me with suggestions/ideas/bugs, create an issue on the 
github repo. I am a student at the UofA and I am always trying to learn more!
Press any key to exit!
'''

ABOUT_MESSAGE = '''
#TODO
'''


def admin_panel():
    user_option_ = str(input(ADMIN_MESSAGE))
    nlp_model_ = None
    if user_option_ == '1':
        tweets_df = pd.read_csv(TWITTER_DF_FILEPATH, header=0, index_col=0, engine='c')
        nlp_model_ = twitter_helper_functions.train_and_save_model(tweets_df['tweet'], tweets_df['label'])
    elif user_option_ == '2':
        twitter_df_path = input('Provide a path to the new training data set')
        tweets_df = pd.read_csv(twitter_df_path, header=0, index_col=0, engine='c')
        nlp_model_ = twitter_helper_functions.train_and_save_model(tweets_df['tweet'], tweets_df['label'])
    elif user_option_ == '3':
        nlp_model_ = twitter_helper_functions.load_model()

    return nlp_model_



def initialize_twitter_api():
    load_dotenv()
    try:
        CONSUMER_KEY = os.getenv('CONSUMER_KEY')
        CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
        ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
        ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    except Exception as e:
        print('This exception occurred', e)

    else:
        twitter_api_ = twitter.Api(consumer_key=CONSUMER_KEY,
                                   consumer_secret=CONSUMER_SECRET,
                                   access_token_key=ACCESS_TOKEN_KEY,
                                   access_token_secret=ACCESS_TOKEN_SECRET)

        return twitter_api_


if __name__ == '__main__':
    twitter_api = initialize_twitter_api()
    while True:
        starting_option = str(input(WELCOME_MESSAGE))
        if starting_option == '1':
            twitter_id = str(input('Provide your user id below with @ symbol (i.e @sharyar) :\n'))
            retrieved_tweets = twitter_helper_functions.get_tweets(api=twitter_api, screen_name=twitter_id)
            retrieved_tweets = twitter_helper_functions.convert_tweets_to_list(retrieved_tweets)
        elif starting_option == '2':
            NLP_model = admin_panel()
        elif starting_option == '3':
            twitter_helper_functions.generate_word_cloud(retrieved_tweets, stopwords=stopwords.words('english'))
        elif starting_option == '4':
            twitter_helper_functions.analyze_and_visualize_tweets(retrieved_tweets, NLP_model)
        elif starting_option.lower() == 'q':
            print(EXIT_MESSAGE)
            time.sleep(3)
            sys.exit()
