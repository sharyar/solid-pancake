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

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Constants:
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
3. Go back!
'''

USER_MESSAGE = '''
***************************
You are in the USer Panel. Please select one of the following options:
1. Provide your twitter id
2. Generate Word Cloud from tweets
3. Do Sentiment Analysis and display a distribution of your tweet sentiments.
4. Go back!
'''

ABOUT_MESSAGE = '''
#TODO
'''

def admin_panel():
    
    while True:
        user_option_ = str(input(ADMIN_MESSAGE))
        if user_option_ == '3':
            break
        elif user_option_ == '1':
            pass

if __name__ == '__main__':
    program_selection = False
    
    while program_selection.lower() != 'q':
        starting_option = str(input(WELCOME_MESSAGE))