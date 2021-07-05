import json

from flask import Blueprint, request

from nimble import db
from nimble.models import Tag, User

from nimble.main.utils import commit_changes_to_db
from nimble.tags.utils import get_all_tags


tag = Blueprint('tag', __name__)


@tag.route('/api/v1/tags', methods=['GET', 'POST'])
def get_all_tags_data():
    topics_data = get_all_tags()
    return json.dumps(topics_data)


@tag.route('/api/v1/tag/create', methods=['GET', 'POST'])
def create_tag():
    username = request.args.get('username')
    name = request.args.get('name')
    
    # Double-check if user is in the database
    user = User.query.filter_by(username=username).first()
    if user is None:
        return "Failure"
    else:
        tag = Tag(name=name)
        db.session.add(tag)
        if commit_changes_to_db():
            return 'Failure'
        else:
            return 'Success'