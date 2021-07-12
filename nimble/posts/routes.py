import sys
import json

from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import current_user

from nimble import db
from nimble.models import Post, User
from nimble.main.utils import commit_changes_to_db
from nimble.posts.utils import get_all_posts, get_post


post = Blueprint('post', __name__)


@post.route('/api/v1/posts', methods=['GET', 'POST'])
def get_all_post_data():
    posts_data = get_all_posts()
    return json.dumps(posts_data)


@post.route('/api/v1/post', methods=['GET', 'POST'])
def get_single_post_data():
    post_id = request.args.get('id', None)
    if post_id is None:
        return 'Failure'
    post_data = get_post(post_id)
    return json.dumps(post_data)


@post.route('/api/v1/posts/create', methods=['GET', 'POST'])
def create_post():
    username = request.args.get('username')
    topic_id = request.args.get('topic_id')
    title = request.args.get('title')
    text = request.args.get('text')
    tags = request.args.get('tags')

    # Double-check if user is in the database
    user = User.query.filter_by(username=username).first()
    if user is None:
        return "Failure"
    else:
        post = Post(topic_id=topic_id, username=user.username, title=title,
                    text=text, tags=tags)
        db.session.add(post)
        if commit_changes_to_db():
            return 'Failure'
        else:
            return 'Success'
