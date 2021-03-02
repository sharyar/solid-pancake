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
import time
import nltk
from nltk.corpus import stopwords
import twitter_helper_functions

nltk.download('stopwords')
stopwords.words('english')
# Constants:
TWITTER_DF_FILEPATH = '../twitter.csv'
# Declare variables used in the program

NLP_model = None
twitter_id = None
retrieved_tweets = None

WELCOME_MESSAGE = '''
Welcome to Solid-Pancake - A Twitter Sentiment Analysis Program
This is the command line version of the tool. A web-based version is
currently under development. 

By: Sharyar Memon

Please select from one of the following options:
1. Do sentiment analysis on your tweets!
2. Admin Access
3. Learn More about the app!
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
    while True:
        user_option_ = str(input(ADMIN_MESSAGE))
        if user_option_ == '1':
            tweets_df = pd.read_csv(TWITTER_DF_FILEPATH, header=0, index_col=0, engine='c')
            NLP_model = twitter_helper_functions.train_and_save_model(tweets_df['tweet'], tweets_df['label'])
        elif user_option_ == '2':
            twitter_df_path = input('Provide a path to the new training data set')
            tweets_df = pd.read_csv(twitter_df_path, header=0, index_col=0, engine='c')
            NLP_model = twitter_helper_functions.train_and_save_model(tweets_df['tweet'], tweets_df['label'])
        elif user_option_ == '3':
            NLP_model = twitter_helper_functions.load_model()
        elif user_option_.lower() == 'q':
            break


if __name__ == '__main__':
    while True:
        starting_option = str(input(WELCOME_MESSAGE))

        if starting_option == '1':
            twitter_id = str(input('Provide your user id below with @ symbol (i.e @sharyar) :\n'))
            retrieved_tweets = twitter_helper_functions.get_tweets(twitter_id)
            retrieved_tweets = twitter_helper_functions.convert_tweets_to_list(retrieved_tweets)
        elif starting_option == '2':
            admin_panel()
        elif starting_option == '3':
            twitter_helper_functions.generate_word_cloud(retrieved_tweets, stopwords=stopwords.words('english'))
        elif starting_option.lower() == 'q':
            print(EXIT_MESSAGE)
            time.sleep(3)
            sys.exit()
