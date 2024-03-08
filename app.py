import os
from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS
from reddit import reddit_posts, auth_url, authenticate, is_authenticated, revoke_auth, get_messages, send_message, reply_to_message_by_id
from project_db import insert_post, insert_user, get_posts
from project_logger import logger
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='client_build')
app.secret_key = os.getenv('SECRET_KEY')
CORS(app, supports_credentials=True)

@app.route('/api/reddit/auth-url')
def reddit_auth_url():
    return jsonify(auth_url())

@app.route('/api/reddit/authenticate', methods=['POST'])
def reddit_authenticate():
    code = request.json['code']
    res = authenticate(code)
    if(res['success'] == 'true'):
        session['REDDIT_REFRESH_TOKEN'] = res['refresh_token']
        session['admin_username'] = res['admin_username']
        return jsonify({'success': 'true', 'admin_username': admin_username})
    else:
        return jsonify(res)
@app.route('/api/reddit/is-authenticated', methods=['GET'])
def reddit_is_authenticated():
    username = session.get('admin_username')
    return jsonify(is_authenticated(username))

@app.route('/api/reddit/revoke-auth', methods=['GET'])
def reddit_revoke_auth():
    token = session.get('REDDIT_REFRESH_TOKEN')
    res = revoke_auth(token)
    if(res['success'] == 'true'):
        session.clear()
    return jsonify(res)


@app.route('/api/reddit/fetch-posts', methods=['POST'])
def get_reddit_posts():
    data = request.get_json()
    subreddit_name = data.get('subreddit', 'Python') 
    max_pages = int(data.get('max_pages', 100))
    postType = data.get('postType', 'top')
    keywords = data.get('keywords', '')
    exactMatch = data.get('exactMatch', False)
    dataFromReddit = reddit_posts(session.get('admin_username'), subreddit_name, keywords, max_pages, postType)
    
    for post in dataFromReddit:
        insert_post(post)
        insert_user(post['author'])

    return jsonify(dataFromReddit)


@app.route('/api/db/posts', methods=['GET'])
def get_db_posts():
    posts = get_posts()
    return jsonify(posts)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify([get_messages()])
    # return send_message('NadeemGorsi', 'Just a test message', 'test message 4')
    # return reply_to_message_by_id('26rcx6t', 'body body2 body2...')
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=5004)