import pytest  # type: ignore
import re

import app as example_tool


@pytest.fixture
def client():
    example_tool.app.testing = True
    client = example_tool.app.test_client()

    with client:
        yield client
    # request context stays alive until the fixture is closed


def test_csrf_token_generate():
    with example_tool.app.test_request_context():
        token = example_tool.csrf_token()
        assert token != ''


def test_csrf_token_save():
    with example_tool.app.test_request_context() as context:
        token = example_tool.csrf_token()
        assert token == context.session['csrf_token']


def test_csrf_token_load():
    with example_tool.app.test_request_context() as context:
        context.session['csrf_token'] = 'test token'
        assert example_tool.csrf_token() == 'test token'


def test_praise(client):
    # default praise
    response = client.get('/praise')
    html = response.get_data(as_text=True)
    assert '<h2>You rock!</h2>' in html

    # extract CSRF token
    match = re.search(r'name="csrf_token" type="hidden" value="([^"]*)"', html)
    assert match is not None
    csrf_token = match.group(1)

    referrer = example_tool.full_url('praise')
    headers = {'Referer': referrer}

    # update praise
    response = client.post('/praise',
                           data={'csrf_token': csrf_token,
                                 'praise': 'How cool!'},
                           headers=headers)
    html = response.get_data(as_text=True)
    assert '<h2>How cool!</h2>' in html
    assert 'You rock!' not in html

    # try to update praise with wrong CSRF token
    response = client.post('/praise',
                           data={'csrf_token': 'wrong ' + csrf_token,
                                 'praise': 'Boo!'},
                           headers=headers)
    html = response.get_data(as_text=True)
    assert '<h2>Boo!</h2>' not in html
    assert '<h2>How cool!</h2>' in html
    assert 'value="Boo!"' in html  # input is repeated
