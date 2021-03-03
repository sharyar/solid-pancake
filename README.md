# solid-pancake
A small app that does sentiment analysis on a user's Twitter feed.

## Current Road Map: 

* Get Twitter API Working - COMPLETED
* Train Simple Gaussian Naive Bayes Model to Classify Tweets into Positive vs Negative - COMPLETED
* Display a word cloud of user's tweets - COMPLETED
* Build a command line application that is able to query a user's Twitter feed, display the word cloud and do simple sentiment analysis. - COMPLETED
* Implement tests to ensure consistent ongoing functionality with changes
* Build Django based site to move from command line to a Web App
* Build a more complex NLP Model to do further sentiment analysis
* Query based on Hashtag

## How to use Command Line Version:

1. Clone this repo to your computer by using "git clone https://github.com/sharyar/solid-pancake.git" in your terminal
2. Install anaconda or pip to install all required dependencies as given in environment.yml 
3. Navigate into the repo folder from your terminal ("cd solid-pancake").
4. Install dependencies and create a new environment by using: "conda env create -f environment.yml"
5. Activate the new environment
6. You will need to create a .env file in the project root directory with your twitter API keys or replace the values within the initialize_twitter_api under the solid_pancake_cli.py. 
7. Run the application: "python solid-pancake/solid_pancake_cli.py"
8. Select option 2 to go to admin panel. Select option 3 to load the pre-trained models. 
9. Select option 1 and enter your twitter id. This will fetch your tweets. 
10. Select option 3 to see a Wordcloud of your tweets
11. Select option 4 to see a pie chart of your positive and negative tweets. 


### .end File Details:

The .env file should have the following lines. Replace the XXXXX with your own keys:
CONSUMER_KEY = 'XXXX'
CONSUMER_SECRET = 'XXXX'
ACCESS_TOKEN_KEY = 'XXXX'
ACCESS_TOKEN_SECRET = 'XXXX'
