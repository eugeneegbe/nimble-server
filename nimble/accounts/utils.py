import sys

from nimble.models import Account

def get_all_accounts():
    """Fetch all proposed useraccounts in the system

    Returns:
        Object: Json objects of all accounts
    """
    all_account = Account.query.all()
    all_post_data = []
    for account in all_account:
        account_data = {}
        account_data['id'] = account.id
        account_data['p_username'] = account.p_username
        account_data['p_email'] = account.p_email
        account_data['status'] = account.status
        all_post_data.append(account_data)
    return all_post_data
