from datetime import datetime
from tech_news.database import search_news


def list_of_tuples(founded_news):
    return [(item["title"], item["url"]) for item in founded_news]


# Requisito 6
def search_by_title(title):
    founded_news = search_news({"title": {"$regex": title, "$options": "i"}})
    return list_of_tuples(founded_news)


# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    founded_news = search_news({"timestamp": {"$regex": date}})
    return list_of_tuples(founded_news)


# Requisito 8
def search_by_source(source):
    founded_news = search_news({"sources": {"$regex": source, "$options": "i"}})
    return list_of_tuples(founded_news)


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
