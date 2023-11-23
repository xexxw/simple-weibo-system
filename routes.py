from flask import request, jsonify
from models import User, Tweet, Follow, Like
from app import app, db


# API
@app.route('/post_content', methods=['POST'])
def post_content_api():
    data = request.get_json()
    user_id = data['user_id']
    content_id = data['content_id']

    user = User.query.get(user_id)
    if user is None:
        user = User(id=user_id)
        db.session.add(user)

    tweet = Tweet(user=user, content_id=content_id)
    db.session.add(tweet)
    db.session.commit()

    return jsonify({"message": "Content posted successfully."})

# 关注用户
@app.route('/follow', methods=['POST'])
def follow_api():
    data = request.get_json()
    follower_id = data['follower_id']
    followee_id = data['followee_id']

    follower = User.query.get(follower_id)
    followee = User.query.get(followee_id)

    if follower is None:
        follower = User(id=follower_id)
        db.session.add(follower)

    if followee is None:
        followee = User(id=followee_id)
        db.session.add(followee)

    follow_relationship = Follow.query.filter_by(follower_id=follower_id, followee_id=followee_id).first()
    if follow_relationship is None:
        follow_relationship = Follow(follower=follower, followee=followee)
        db.session.add(follow_relationship)

    db.session.commit()

    return jsonify({"message": "Followed successfully."})

# 取消关注用户
@app.route('/unfollow', methods=['POST'])
def unfollow_api():
    data = request.get_json()
    follower_id = data['follower_id']
    followee_id = data['followee_id']

    follow_relationship = Follow.query.filter_by(follower_id=follower_id, followee_id=followee_id).first()
    if follow_relationship:
        db.session.delete(follow_relationship)
        db.session.commit()

    return jsonify({"message": "Unfollowed successfully."})

# 获取用户Feed
@app.route('/get_feed/<int:user_id>', methods=['GET'])
def get_feed_api(user_id):
    user = User.query.get(user_id)
    if user:
        feed = [tweet.content_id for tweet in user.tweets]
        return jsonify({"feed": feed})
    else:
        return jsonify({"error": "User not found."}), 404

# 点赞微博
@app.route('/like', methods=['POST'])
def like_api():
    data = request.get_json()
    user_id = data['user_id']
    content_id = data['content_id']

    user = User.query.get(user_id)
    tweet = Tweet.query.filter_by(content_id=content_id).first()

    if user and tweet:
        like_relationship = Like.query.filter_by(user_id=user_id, content_id=tweet.id).first()
        if like_relationship is None:
            like_relationship = Like(user=user, tweet=tweet)
            db.session.add(like_relationship)
            db.session.commit()

        return jsonify({"likes": len(tweet.likes)})
    else:
        return jsonify({"error": "User or tweet not found."}), 404

# 取消点赞
@app.route('/unlike', methods=['POST'])
def unlike_api():
    data = request.get_json()
    user_id = data['user_id']
    content_id = data['content_id']

    user = User.query.get(user_id)
    tweet = Tweet.query.filter_by(content_id=content_id).first()

    if user and tweet:
        like_relationship = Like.query.filter_by(user_id=user_id, content_id=tweet.id).first()
        if like_relationship:
            db.session.delete(like_relationship)
            db.session.commit()

        return jsonify({"likes": len(tweet.likes)})
    else:
        return jsonify({"error": "User or tweet not found."}), 404

# 获取热门微博
@app.route('/get_hot_contents', methods=['GET'])
def get_hot_contents_api():
    all_tweets = Tweet.query.all()
    hot_contents = nlargest(15, all_tweets, key=lambda x: len(x.likes))
    hot_contents_ids = [tweet.content_id for tweet in hot_contents]

    return jsonify({"hot_contents": hot_contents_ids})

if __name__ == '__main__':
    app.run(debug=True)
