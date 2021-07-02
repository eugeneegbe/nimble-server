import sys
import flask
import mwoauth
import requests_oauthlib
import mwapi
import toolforge

from nimble import db, app

def commit_changes_to_db():
    """
    Test for the success of a database commit operation.

    """
    try:
        db.session.commit()
    except Exception as e:
        # TODO: We could add a try catch here for the error
        print('-------------->>>>>', file=sys.stderr)
        print(str(e), file=sys.stderr)
        db.session.rollback()
        # for resetting non-commited .add()
        db.session.flush()
        return True
    return False


def authenticated_session():
    user_agent = toolforge.set_user_agent(
    'example-tool',
    email='agboreugene@gmail.com')

    if 'oauth' in app.config:
        oauth_config = app.config['oauth']
        consumer_token = mwoauth.ConsumerToken(oauth_config['consumer_key'],
                                                oauth_config['consumer_secret'])
        index_php = 'https://meta.wikimedia.org/w/index.php'

    if 'oauth_access_token' not in flask.session:
        return None

    access_token = mwoauth.AccessToken(
        **flask.session['oauth_access_token'])
    auth = requests_oauthlib.OAuth1(client_key=consumer_token.key,
                                    client_secret=consumer_token.secret,
                                    resource_owner_key=access_token.key,
                                    resource_owner_secret=access_token.secret)
    return mwapi.Session(host='https://meta.wikimedia.org',
                        auth=auth,
                        user_agent=user_agent)