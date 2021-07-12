import json

from flask import Blueprint, session, request

from nimble.main.utils import commit_changes_to_db

from nimble import db
from nimble.models import Reply, User
from nimble.replies.utils import get_all_replies


reply = Blueprint('reply', __name__)


@reply.route('/api/v1/replies/create', methods=['GET', 'POST'])
def create_reply():
    username = request.args.get('username')
    post_id = request.args.get('post_id')
    text = request.args.get('text')
    
    # Double-check if user is in the database
    user = User.query.filter_by(username=username).first()
    if user is None:
        return "Failure"
    else:
        reply = Reply(username=username, post_id=post_id, text=text)
        db.session.add(reply)
        if commit_changes_to_db():
            return 'Failure'
        else:
            return 'Success'


@reply.route('/api/v1/replies', methods=['GET', 'POST'])
def get_all_reply_data():
    post_id = request.args.get('post_id', None);
    replies_data = get_all_replies(post_id)
    return json.dumps(replies_data)
