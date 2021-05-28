from flask import render_template, request, redirect, url_for, flash, abort, session,jsonify, Blueprint, Flask, send_file
import json
import os
import twitter_helper_functions
import nltk
from nltk.corpus import stopwords
from dotenv import load_dotenv
import twitter
import re
# Constants:
TWITTER_DF_FILEPATH = '../twitter.csv'
# Declare variables used in the program

NLP_model = None
twitter_id = None
retrieved_tweets = None
twitter_api = None

def initialize_twitter():
    """Starts twitter api by loading all the required key

    Returns:
        [object]: instance of twitter api that will be used to access data
    """
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
    nltk.download('stopwords')
    stopwords.words('english')

    return twitter_api_



#### Flask APP ####
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret = 'gibbers'

twitter_api = initialize_twitter()

@app.route('/')
def home():
    return render_template('home.html', twitter_username=session.keys())


# Functional work to query and process twitter data
@app.route('/your-twitter', methods=['GET', 'POST'])
def your_twitter():
    # Delete old wordcloud file if it exists:
    delete_wordcloud()
    
    if request.method == 'POST':
        usernames = {}
        
        if os.path.exists('usernames.json'):
            with open('usernames.json', 'r') as f:
                usernames = json.load(f)
        
        if request.form['username'] in usernames.keys():
            flash('You have searched this username before!')
            # todo return to display results
            
        # ask for twitter data and store it temporarily 
        requested_name = request.form['username']
        # query twitter
        tweets = twitter_helper_functions.get_tweets(twitter_api, requested_name)
        tweets = twitter_helper_functions.convert_tweets_to_list(tweets)
        tweets = [re.sub(r'https\S+', '', x) for x in tweets]
        
        # generate wordcloud
        twitter_helper_functions.generate_wordcloud_web(tweets, requested_name)
        
        path_wordcloud = f'static/images/{requested_name}-wordcloud.png'
        
        nlp_model = twitter_helper_functions.load_model()
        bar_chart = twitter_helper_functions.analyze_and_visualize_tweets_web(tweets, nlp_model)
        
        data_dict = {
            'wc':path_wordcloud,
            'bc':bar_chart
        }
        
        return render_template('twitter.html', data=data_dict)
    
    else:
        return redirect(url_for("home"))
        


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run()
    
    
def delete_wordcloud():
    dir_name = 'static/images'
    file_list = os.listdir(dir_name)
    
    for file in file_list:
        if file.endswith('.png'):
            os.remove(os.path.join(dir_name, file))
