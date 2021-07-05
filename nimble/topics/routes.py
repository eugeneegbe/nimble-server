import json

from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import current_user

from nimble import db
from nimble.models import Topic, User

from nimble.main.utils import commit_changes_to_db
from nimble.topics.utils import get_all_topics



topic = Blueprint('topic', __name__)


@topic.route('/api/v1/topics', methods=['GET', 'POST'])
def get_all_topics_data():
    topics_data = get_all_topics()
    return json.dumps(topics_data)


@topic.route('/api/v1/topic/create', methods=['GET', 'POST'])
def create_topic():
    username = request.args.get('username')
    name = request.args.get('name')
    
    # Double-check if user is in the database
    user = User.query.filter_by(username=username).first()
    if user is None or user.role is False:
        return "Failure"
    else:
        topic = Topic(name=name)
        db.session.add(topic)
        if commit_changes_to_db():
            return 'Failure'
        else:
            return 'Success'