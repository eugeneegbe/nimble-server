from nimble.models import Tag


def get_all_tags():
    """Fetch all Tags in the system

    Returns:
        Object: Json objects of all tags
    """
    all_tags = Tag.query.all()
    all_tags_data = []
    for tag in all_tags:
        tag_data = {}
        tag_data['id'] = tag.id
        tag_data['name'] = tag.name
        all_tags_data.append(tag_data)
    return all_tags_data
