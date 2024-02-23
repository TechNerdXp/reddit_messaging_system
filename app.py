from flask import Flask, jsonify, request
from flask_cors import CORS
from reddit import reddit_posts
from filters import filter_posts

app = Flask(__name__)
CORS(app)

@app.route('/reddit', methods=['GET'])
def get_reddit_posts():
    subreddit_name = request.args.get('subreddit', 'Python') 
    limit = int(request.args.get('limit', 10))
    postType = request.args.get('postType', 'top')
    keywords = request.args.get('keywords', '')
    exactMatch = request.args.get('exactMatch', False)
    dataFromReddit = reddit_posts(subreddit_name, limit, postType)
    filteredData = filter_posts(dataFromReddit, keywords, exactMatch)
    
    #model of dataFormReddit
    # [
    #     {
    #         "author": "@AutoModerator",
    #         "html": "<!-- SC_OFF --><div class=\"md\"><h1>Weekly Thread: What&#39;s Everyone Working On This ",
    #         "id": "1atgacs",
    #         "text": "# Weekly Thread: What's Everyone Working On This Week? redict stock ",
    #         "title": "Sunday Daily Thread: What's everyone working on this week?"
    #     },
    #     {
    #         "author": "@AutoModerator",
    #         "html": "<!-- SC_OFF --><div class=\"md\"><h1>Weekly Thread: Meta ",
    #         "id": "1axm27l",
    #         "text": "# Weekly Thread: Meta Discussions and Free Talk Friday \ud83c\udf99\ufe0f\n\"
    #     },
    #     {
    #         "author": "@Hyperdiv-io",
    #         "html": "<!-- SC_OFF --><div class=\"md\"><p>Hi guys! I&#39;d like to shar",
    #         "id": "1axgbg6",
    #         "text": "Hi guys! I'd like to share a reactive web UI framework I've been working ",
    #         "title": "Hyperdiv: Reactive web UI framework for Python"
    #     }
    # ]
    # I want an SQLIte module for above data model 
    
    return jsonify(dataFromReddit)

if __name__ == '__main__':
    app.run(debug=True)
