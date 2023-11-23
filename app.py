from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///microblog.db'
db = SQLAlchemy(app)

# 导入其他模块
from models import User, Tweet, Follow, Like
from routes import post_content_api, follow_api, unfollow_api, get_feed_api, like_api, unlike_api, get_hot_contents_api

# 创建数据库表
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
