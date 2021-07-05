from nimble.models import Reply


def get_all_replies():
    """Fetch all posts in the system

    Returns:
        Object: Json objects of all posts
    """
    all_replies = Reply.query.all()
    all_reply_data = []
    for reply in all_replies:
        reply_data = {}
        reply_data['id'] = reply.id
        reply_data['post_id'] = reply.post_id
        reply_data['username'] = reply.username
        reply_data['text'] = reply.text
        reply_data['timestamp'] = reply.timestamp.strftime('%Y-%m-%d %H:%M') 
        all_reply_data.append(reply_data)
    return all_reply_data
