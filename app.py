from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///microblog.db'
db = SQLAlchemy(app)

if __name__ == '__main__':
    with app.app_context():
        from routes import post_content_api, follow_api, unfollow_api, get_feed_api, like_api, unlike_api, get_hot_contents_api
        db.create_all()
    app.run(debug=True)
