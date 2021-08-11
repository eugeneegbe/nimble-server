import sys

import wikipediaapi
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


def get_category_articles(category, level=0, max_level=1):
    articles = []
    wiki_wiki = wikipediaapi.Wikipedia('en')
    cat = wiki_wiki.page("Category:" + category)
    for c in cat.categorymembers.values():
        if ':' not in c.title:
            articles.append(c.title)
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                get_category_articles(level=level + 1, max_level=max_level)
    return articles


def build_article_url(article):
    base_url = 'https://en.wikipedia.org/wiki/'
    return base_url + article.replace(' ', '_')
