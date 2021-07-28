import sys

from nimble.models import Article

def get_all_articles():
    """Fetch all articles in the system

    Returns:
        Object: Json objects of all articles
    """
    all_article = Article.query.filter_by(status=0).all()
    print(all_article, file=sys.stderr)
    all_article_data = []
    for article in all_article:
        article_data = {}
        article_data['id'] = article.id
        article_data['name'] = article.name
        article_data['url'] = article.url
        article_data['hint'] = article.hint
        article_data['status'] = article.status
        article_data['created'] = article.created.strftime('%Y-%m-%d %H:%M')

        all_article_data.append(article_data)
    return all_article_data[0:4]
