import sys
import json

from flask import Blueprint, request

from nimble import db
from nimble.models import Account, User
from nimble.main.utils import commit_changes_to_db
from nimble.accounts.utils import get_all_accounts, build_status_error


account = Blueprint('account', __name__)


@account.route('/api/v1/accounts', methods=['GET', 'POST'])
def get_all_accounts_data():
    accounts_data = get_all_accounts()
    return json.dumps(accounts_data)


@account.route('/api/v1/accounts/create', methods=['GET', 'POST'])
def create_account():
    p_username = request.args.get('p_username')
    p_email = request.args.get('p_email')

    # Double-check if user is in the database
    account = Account.query.filter_by(p_username=p_username).first()
    if account is None:
        account = Account(p_username=p_username, p_email=p_email)
        db.session.add(account)
        if commit_changes_to_db():
            return build_status_error()
        else:
            return 'Success'
    else:
        return build_status_error()
