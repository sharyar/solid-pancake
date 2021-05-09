from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint, Flask
import json
import os.path

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', twitter_username=session.keys())

@app.route('/your-twitter', methods=['GET', 'POST'])
def your_twitter():
    if request.method == 'POST':
        usernames = {}
        
        if os.path.exists('usernames.json'):
            with open('usernames.json', 'r') as f:
                usernames = json.load(f)
        
        if request.form['username'] in usernames.keys():
            flash('You have searched this username before!')
            # todo return to display results
            

@app.route('/<string:username>')
def results():
    return render_template('results.html', twitter_data=twitter_user_data)


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')