import os

import yaml
import flask
from flask import request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

__dir__ = os.path.dirname(__file__)
try:
    with open(os.path.join(__dir__, 'config.yaml')) as config_file:
        app.config.update(yaml.safe_load(config_file))
except FileNotFoundError:
    print('config.yaml file not found, assuming local development setup')
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(64))
    app.secret_key = random_string


# Another secret key will be generated later
app.config['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY']
app.config['TEMPLATES_AUTO_RELOAD']

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.home'
login_manager.login_message = 'You Need to Login to Access This Page!'
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
	return None


# we import all our blueprint routes here
from nimble.main.routes import main
from nimble.users.routes import users
from nimble.posts.routes import post
from nimble.replies.routes import reply
from nimble.topics.routes import topic
from nimble.tags.routes import tag
from nimble.accounts.routes import account
from nimble.articles.routes import article


# Here we register the various blue_prints of our app
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(post)
app.register_blueprint(reply)
app.register_blueprint(topic)
app.register_blueprint(tag)
app.register_blueprint(account)
app.register_blueprint(article)
