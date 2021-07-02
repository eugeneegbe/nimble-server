import os
import sys
import flask

from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import current_user

from .utils import authenticated_session


main = Blueprint('main', __name__)


@main.route('/')
def index():
    session = authenticated_session()
    if session:
        userinfo = session.get(action='query',
                                meta='userinfo',
                                uiprop='options')['query']['userinfo']
        name = userinfo['name']
    else:
        name = 'Anonymous' 
    return flask.render_template('index.html',
                                    name=name)
