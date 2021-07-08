from uuid import uuid4

def generate_random_token():
    rand_token = uuid4()
    return str(rand_token)
