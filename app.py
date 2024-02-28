import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from reddit import reddit_posts, auth_url, authenticate, is_authenticated, revoke_auth
from filters import filter_posts
from project_db import insert_post, insert_user, get_posts
from project_logger import logger
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
CORS(app, supports_credentials=True)


@app.route('/api/reddit/auth-url')
def reddit_auth_url():
    return jsonify(auth_url())

@app.route('/api/reddit/authenticate', methods=['POST'])
def reddit_authenticate():
    code = request.json['code']
    
    return jsonify(authenticate(code))

@app.route('/api/reddit/is-authenticated', methods=['GET'])
def reddit_is_authenticated():
    return jsonify(is_authenticated())

@app.route('/api/reddit/revoke-auth', methods=['GET'])
def reddit_revoke_auth():
    return jsonify(revoke_auth())

@app.route('/api/reddit/fetch-posts', methods=['POST'])
def get_reddit_posts():
    data = request.get_json()
    subreddit_name = data.get('subreddit', 'Python') 
    max_pages = int(data.get('max_pages', 100))
    postType = data.get('postType', 'top')
    keywords = data.get('keywords', '')
    exactMatch = data.get('exactMatch', False)
    dataFromReddit = reddit_posts(subreddit_name, max_pages, postType)
    filteredData = filter_posts(dataFromReddit, keywords, exactMatch)
    
    for post in filteredData:
        insert_post(post)
        insert_user(post['author'])

    return jsonify(filteredData)


@app.route('/api/db/posts', methods=['GET'])
def get_db_posts():
    posts = get_posts()
    return jsonify(posts)

    
if __name__ == '__main__':
    app.run(debug=True)
