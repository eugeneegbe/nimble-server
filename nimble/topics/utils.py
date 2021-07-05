from nimble.models import Topic


def get_all_topics():
    """Fetch all Topics in the system

    Returns:
        Object: Json objects of all topics
    """
    all_topics = Topic.query.all()
    all_topic_data = []
    for topic in all_topics:
        topic_data = {}
        topic_data['id'] = topic.id
        topic_data['name'] = topic.name
        all_topic_data.append(topic_data)
    return all_topic_data
