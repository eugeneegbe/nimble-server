import sys
import json

from flask import Blueprint, request, render_template, flash, redirect, url_for

from nimble import db
from nimble.articles.forms import ArticleImportForm
from nimble.models import Article, User
from nimble.main.utils import commit_changes_to_db
from nimble.articles.utils import get_all_articles, get_category_articles, build_article_url
from nimble.main.utils import authenticated_session


article = Blueprint('article', __name__)


@article.route('/api/v1/articles', methods=['GET', 'POST'])
def get_all_articles_data():
    articles_data = get_all_articles()
    return json.dumps(articles_data)


@article.route('/api/v1/articles/import', methods=['GET', 'POST'])
def import_articles():
    session = authenticated_session()
    admin = False
    if session:
        userinfo = session.get(action='query',
                                meta='userinfo',
                                uiprop='options')['query']['userinfo']
        name = userinfo['name']
    else:
        name = 'Anonymous'
    user = User.query.filter_by(username=name).first()
    if user is None or user.role is False:
        return redirect(url_for('main.index'))

    category_articles = []
    some_articles = False
    done_adding = False
    category_value = ''
    form = ArticleImportForm()
    if form.is_submitted():
        category_value = form.category_name.data
        category_articles = get_category_articles(category_value)
        if len(category_articles) > 0:
            some_articles = True
            for article in category_articles:
                # Check if article exists before adding
                test_article = Article.query.filter_by(name=article).first()
                if test_article is None:
                    new_article = Article(name=article,
                                            hint=category_value,
                                            url=build_article_url(article))
                    db.session.add(new_article)
            if commit_changes_to_db():
                flash('Articles could not be added now', 'info')
            else:
                done_adding = True
                flash('Great! articles were added', 'success')
    return render_template('articles/article_import.html',
                            form=form,
                            category_value=category_value,
                            some_articles=some_articles,
                            done_adding=done_adding,
                            articles=category_articles)
