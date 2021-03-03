# solid-pancake
A small app that does sentiment analysis on a user's Twitter feed.

## Current Road Map: 

-[x] Get Twitter API Working 
-[x] Train Simple Gaussian Naive Bayes Model to Classify Tweets into Positive vs Negative
-[x] Display a word cloud of user's tweets
-[x] Build a command line application that is able to query a user's Twitter feed, display the word cloud and do simple sentiment analysis.
-[ ] Implement tests to ensure consistent ongoing functionality with changes
-[ ] Build Django based site to move from command line to a Web App
-[ ] Build a more complex NLP Model to do further sentiment analysis
-[ ] Query based on Hashtag

## How to use Command Line Version:

1. Clone this repo to your computer by using "git clone https://github.com/sharyar/solid-pancake.git" in your terminal
2. Install anaconda or pip to install all required dependencies as given in environment.yml 
3. Navigate into the repo folder from your terminal ("cd solid-pancake").
4. Install dependencies and create a new environment by using: "conda env create -f environment.yml"
5. Activate the new environment
6. Run the application: "python solid-pancake/solid_pancake_cli.py"
7. Select option 2 to go to admin panel. Select option 3 to load the pre-trained models. 
8. Select option 1 and enter your twitter id. This will fetch your tweets. 
9. Select option 3 to see a Wordcloud of your tweets
10. Select option 4 to see a pie chart of your positive and negative tweets. 