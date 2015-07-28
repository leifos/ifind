from django import template

register = template.Library()


@register.filter
def linebreaksbrbr(article, service):
    article = article.replace('``', '"')
    article = article.replace('\'\'', '"')
    article = article.replace(' _ ', ' ')

    if 'Xinhua' in service:
        return article.replace('\n \n', '<p></p>')

    if 'Associated Press' in service:
        article = article.replace('\n\t   ', '<p></p>')
        article = article.replace('\n   ', '<p></p>')
        return article.replace(' \n\t', '<p></p>')

    # Assume New York Times News Service formatting
    return article.replace('\n   ', '<p></p>')


@register.filter
def removeps(article):
    article = article.replace('&lt;p&gt;', '')
    article = article.replace('&lt;/p&gt;', '')
    article = article.replace('/p&gt;', '')
    article = article.replace('p&gt;', '')
    article = article.replace('&lt;p', '')
    return article