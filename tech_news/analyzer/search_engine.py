from datetime import datetime
from tech_news.database import search_news


def list_of_tuples(found_news):
    return [(item["title"], item["url"]) for item in found_news]


def regex_option(title_or_source_or_category):
    return {"$regex": title_or_source_or_category, "$options": "i"}


# Requisito 6
def search_by_title(title):
    found_news = search_news({"title": regex_option(title)})
    return list_of_tuples(found_news)


# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    found_news = search_news({"timestamp": {"$regex": date}})
    return list_of_tuples(found_news)


# Requisito 8
def search_by_source(source):
    found_news = search_news({"sources": regex_option(source)})
    return list_of_tuples(found_news)


# Requisito 9
def search_by_category(category):
    found_news = search_news({"categories": regex_option(category)})
    return list_of_tuples(found_news)
