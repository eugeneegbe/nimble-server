import sys
import json

from flask import Blueprint, request

from nimble import db
from nimble.models import Article
from nimble.main.utils import commit_changes_to_db
from nimble.articles.utils import get_all_articles


article = Blueprint('article', __name__)


@article.route('/api/v1/articles', methods=['GET', 'POST'])
def get_all_articles_data():
    articles_data = get_all_articles()
    return json.dumps(articles_data)