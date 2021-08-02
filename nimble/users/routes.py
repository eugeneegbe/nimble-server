import flask
import mwapi
import mwoauth
import os
import random
import requests_oauthlib
import string
import toolforge
import yaml
import json

from flask import Blueprint, request
from nimble import app, db
from nimble.models import User
from nimble.main.utils import authenticated_session, commit_changes_to_db
from nimble.users.utils import generate_random_token

users = Blueprint('users', __name__)


user_agent = toolforge.set_user_agent(
    'example-tool',
    email='agboreugene@gmail.com')


if 'oauth' in app.config:
    oauth_config = app.config['oauth']
    consumer_token = mwoauth.ConsumerToken(oauth_config['consumer_key'],
                                            oauth_config['consumer_secret'])
    index_php = 'https://meta.wikimedia.org/w/index.php'


@app.template_global()
def csrf_token():
    if 'csrf_token' not in flask.session:
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(64))
        flask.session['csrf_token'] = random_string
    return flask.session['csrf_token']


@app.template_global()
def form_value(name):
    if 'repeat_form' in flask.g and name in flask.request.form:
        return (flask.Markup(r' value="') +
                flask.Markup.escape(flask.request.form[name]) +
                flask.Markup(r'" '))
    else:
        return flask.Markup()


@app.template_global()
def form_attributes(name):
    return (flask.Markup(r' id="') +
            flask.Markup.escape(name) +
            flask.Markup(r'" name="') +
            flask.Markup.escape(name) +
            flask.Markup(r'" ') +
            form_value(name))


@app.template_filter()
def user_link(user_name):
    user_href = 'https://www.wikidata.org/wiki/User:'
    return (flask.Markup(r'<a href="' + user_href) +
            flask.Markup.escape(user_name.replace(' ', '_')) +
            flask.Markup(r'">') +
            flask.Markup(r'<bdi>') +
            flask.Markup.escape(user_name) +
            flask.Markup(r'</bdi>') +
            flask.Markup(r'</a>'))


@app.template_global()
def authentication_area():
    if 'oauth' not in app.config:
        return flask.Markup()

    session = authenticated_session()
    if session is None:
        return (flask.Markup(r'<a id="login" class="navbar-text" href="') +
                flask.Markup.escape(flask.url_for('login')) +
                flask.Markup(r'">Log in</a>'))

    userinfo = session.get(action='query',
                        meta='userinfo')['query']['userinfo']
    return (flask.Markup(r'<span class="navbar-text">Logged in as ') +
            user_link(userinfo['name']) +
            flask.Markup(r'</span>'))


@users.route('/login')
def login():
    redirect, request_token = mwoauth.initiate(index_php,
                                                consumer_token,
                                                user_agent=user_agent)
    flask.session['oauth_request_token'] = dict(zip(request_token._fields,
                                                    request_token))
    return_url = flask.request.referrer
    if return_url and return_url.startswith(full_url('main.index')):
        flask.session['oauth_redirect_target'] = return_url
    return flask.redirect(redirect)


@users.route('/oauth-callback')
def oauth_callback():
    oauth_request_token = flask.session.pop('oauth_request_token', None)
    if oauth_request_token is None:
        already_logged_in = 'oauth_access_token' in flask.session
        query_string = flask.request.query_string\
                                    .decode(flask.request.url_charset)
        return flask.redirect("https://nimble.toolforge.org/get-started?oauth=failed", code=302)
    request_token = mwoauth.RequestToken(**oauth_request_token)
    access_token = mwoauth.complete(index_php,
                                    consumer_token,
                                    request_token,
                                    flask.request.query_string,
                                    user_agent=user_agent)
    flask.session['oauth_access_token'] = dict(zip(access_token._fields,
                                                    access_token))
    flask.session.pop('csrf_token', None)
    redirect_target = flask.session.pop('oauth_redirect_target', None)
    # return flask.redirect(redirect_target or flask.url_for('main.index'))
    session = authenticated_session()
    if session:
        userinfo = session.get(action='query',
                                meta='userinfo',
                                uiprop='options')['query']['userinfo']
        user_name = userinfo['name']
        user = User.query.filter_by(username=user_name).first()
        user_token = generate_random_token()
        if user is None:
            userinfo = session.get(action='query',
                            meta='userinfo',
                            uiprop='options')['query']['userinfo']
            new_user = User(username=userinfo['name'], token=user_token)
            db.session.add(new_user)
            if commit_changes_to_db(): # success
                flask.flash('Error adding user to database')
    userinfo = session.get(action='query',
                                    meta='userinfo',
                                    uiprop='options')['query']['userinfo']

    user_token = User.query.filter_by(username=userinfo['name']).first().token
    return flask.redirect("https://nimble.toolforge.org/oauth/callback?token=" + str(user_token), code=302)


@users.route('/api/v1/verify_token', methods=['GET','POST'])
def get_current_user_info():
    token = request.args.get('token')

    user = User.query.filter_by(token=token).first()
    if not user:
        return "Failure"
    else:
        user_infomration = {}   
        user_info_obj = {}

        user_info_obj['username'] = user.username
        user_info_obj['lang'] = user.pref_lang
        user_info_obj['role'] = user.role
        user_info_obj['current_stage'] = user.current_stage

        user_infomration['user'] = user_info_obj
        return json.dumps(user_infomration)


@users.route('/api/v1/add_stage', methods=['GET','POST'])
def add_user_stage():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    stage_info = {}
    if user is None:
        return "Failure"
    user.current_stage = user.current_stage + 1
    if commit_changes_to_db():
        return 'Failure'
    else:
        stage_info['username'] = user.username
        stage_info['current_stage'] = user.current_stage
        return json.dumps(stage_info)


@users.route('/logout')
def logout():
    flask.session.pop('oauth_access_token', None)
    return flask.redirect(flask.url_for('main.index'))


def full_url(endpoint, **kwargs):
    scheme = flask.request.headers.get('X-Forwarded-Proto', 'http')
    return flask.url_for(endpoint, _external=True, _scheme=scheme, **kwargs)


def submitted_request_valid():
    """Check whether a submitted POST request is valid.

    If this method returns False, the request might have been issued
    by an attacker as part of a Cross-Site Request Forgery attack;
    callers MUST NOT process the request in that case.
    """
    real_token = flask.session.get('csrf_token')
    submitted_token = flask.request.form.get('csrf_token')
    if not real_token:
        # we never expected a POST
        return False
    if not submitted_token:
        # token got lost or attacker did not supply it
        return False
    if submitted_token != real_token:
        # incorrect token (could be outdated or incorrectly forged)
        return False
    return True


# If you don’t want to handle CSRF protection in every POST handler,
# you can instead uncomment the @app.before_request decorator
# on the following function,
# which will raise a very generic error for any invalid POST.
# Otherwise, you can remove the whole function.
# @app.before_request
def require_valid_submitted_request():
    if flask.request.method == 'POST' and not submitted_request_valid():
        return 'CSRF error', 400  # stop request handling
    return None  # continue request handling


@app.after_request
def deny_frame(response):
    """Disallow embedding the tool’s pages in other websites.

    Not every tool can be usefully embedded in other websites, but
    allowing embedding can expose the tool to clickjacking
    vulnerabilities, so err on the side of caution and disallow
    embedding. This can be removed (possibly only for certain pages)
    as long as other precautions against clickjacking are taken.
    """
    response.headers['X-Frame-Options'] = 'deny'
    return response
