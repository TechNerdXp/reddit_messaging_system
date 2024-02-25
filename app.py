from flask import Flask, jsonify, request
from flask_cors import CORS
from reddit import reddit_posts, auth_url, authenticate, is_authenticated
from filters import filter_posts
from project_db import insert_post, insert_user, get_posts
from project_logger import logger


app = Flask(__name__)
CORS(app)

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

@app.route('/reddit', methods=['GET'])
def get_reddit_posts():
    subreddit_name = request.args.get('subreddit', 'Python') 
    limit = int(request.args.get('limit', 10))
    postType = request.args.get('postType', 'top')
    keywords = request.args.get('keywords', '')
    exactMatch = request.args.get('exactMatch', False)
    dataFromReddit = reddit_posts(subreddit_name, limit, postType)
    filteredData = filter_posts(dataFromReddit, keywords, exactMatch)
    
    for post in filteredData:
        insert_post(post)
        insert_user(post['author'])

    return jsonify(filteredData)

@app.route('/posts', methods=['GET'])
def get_db_posts():
    posts = get_posts()
    return jsonify(posts)

    
if __name__ == '__main__':
    app.run(debug=True)
