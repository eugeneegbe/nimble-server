import sys
from nimble.models import Post

def get_all_posts():
    """Fetch all posts in the system

    Returns:
        Object: Json objects of all posts
    """
    all_post = Post.query.all()
    all_post_data = []
    for post in all_post:
        post_data = {}
        post_data['id'] = post.id
        post_data['title'] = post.title
        post_data['username'] = post.username
        post_data['text'] = post.text
        post_data['tags'] = post.tags.split(',')
        post_data['timestamp'] = post.timestamp.strftime('%Y-%m-%d %H:%M') 
        all_post_data.append(post_data)
    return all_post_data


def get_post(id):
    post_data = Post.query.filter_by(id=id).first()
    if post_data is None:
        return "Failure"
    else:
        post_json_arr = {}
        post_object = {}
        post_object['id'] = post_data.id
        post_object['title'] = post_data.title
        post_object['username'] = post_data.username
        post_object['text'] = post_data.text
        post_object['tags'] = post_data.tags.split(',')
        post_object['timestamp'] = post_data.timestamp.strftime('%Y-%m-%d %H:%M')
        post_json_arr['post'] = post_object
        return post_json_arr