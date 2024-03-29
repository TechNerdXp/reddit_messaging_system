import os
from flask import Flask, Response, jsonify, request, send_from_directory, session
from flask_cors import CORS
from reddit import reddit_posts, auth_url, authenticate, is_authenticated, revoke_auth, get_messages, send_message, send_reply
from project_db import ( 
    insert_post, insert_user, get_posts, get_configs, get_config, update_config,
    insert_admin_and_subreddit, get_admins_and_subreddits, update_admin_and_subreddit, delete_admin_and_subreddit
)
from project_logger import logger
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='client_build')
# app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
CORS(app, supports_credentials=True)

@app.route('/api/reddit/auth-url')
def reddit_auth_url():
    return jsonify(auth_url())

@app.route('/api/reddit/authenticate', methods=['POST'])
def reddit_authenticate():
    code = request.json['code']
    res = authenticate(code)
    if(res['success']):
        session['REDDIT_REFRESH_TOKEN'] = res['refresh_token']
        session['admin_username'] = res['admin_username']
        return jsonify({'success': True, 'admin_username': res['admin_username']})
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
    if(res['success']):
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
    dataFromReddit = reddit_posts(session.get('admin_username'), subreddit_name, keywords, None, max_pages, postType)
    
    for post in dataFromReddit:
        insert_post(post)
        insert_user(post['author'])

    return jsonify(dataFromReddit)

@app.route('/api/db/posts', methods=['GET'])
def get_db_posts():
    posts = get_posts(limit=100)
    return jsonify(posts)

@app.route('/api/configs', methods=['GET'])
def get_configurations():
    configs = get_configs()
    return jsonify(configs)

@app.route('/api/configs/<key>', methods=['PUT'])
def update_configuration(key):
    value = request.json['value']
    update_config(key, value)
    return jsonify({'status': 'success'})


@app.route('/api/admins-and-subreddits', methods=['POST'])
def create_admin_and_subreddit():
    data = request.get_json()
    insert_admin_and_subreddit(data['username'], data['subreddits'], data['keywords'])
    return jsonify({'message': 'Admin and subreddit created successfully'}), 201

@app.route('/api/admins-and-subreddits', methods=['GET'])
def read_admins_and_subreddits():
    admins_and_subreddits = get_admins_and_subreddits()
    return jsonify(admins_and_subreddits), 200

@app.route('/api/admins-and-subreddits/<id>', methods=['PUT'])
def update_admin_and_subreddit_route(id):
    data = request.get_json()
    update_admin_and_subreddit(id, data['username'], data['subreddits'], data['keywords'])
    return jsonify({'message': 'Admin and subreddit updated successfully'}), 200

@app.route('/api/admins-and-subreddits/<id>', methods=['DELETE'])
def delete_admin_and_subreddit_route(id):
    delete_admin_and_subreddit(id)
    return jsonify({'message': 'Admin and subreddit deleted successfully'}), 200

@app.route('/info_logs')
def info_logs():
    try:
        with open('logs/info.log', 'r') as f:
            content = f.read()
        return Response(content, mimetype='text/plain')
    except FileNotFoundError:
        return "The file does not exist", 404

@app.route('/error_logs')
def error_logs():
    try:
        with open('logs/error.log', 'r') as f:
            content = f.read()
        return Response(content, mimetype='text/plain')
    except FileNotFoundError:
        return "The file does not exist", 404


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify([get_messages()])
    # return send_message('NadeemGorsi', 'Just a test message', 'test message 4')
    # return reply_to_message_by_id('26rcx6t', 'body body2 body2...')
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != '' and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=5004)
