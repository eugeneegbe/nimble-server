import sys

from nimble.models import Article

def get_all_articles():
    """Fetch all articles in the system

    Returns:
        Object: Json objects of all articles
    """
    all_article = Article.query.all()
    all_article_data = []
    for article in all_article:
        article_data = {}
        article_data['id'] = article.id
        article_data['name'] = article.name
        article_data['url'] = article.url
        article_data['created'] = article.created.strftime('%Y-%m-%d %H:%M') 

        all_article_data.append(article_data)
    print(all_article_data, file=sys.stderr)
    return all_article_data
