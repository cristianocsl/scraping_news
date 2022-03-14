from parsel import Selector
import requests
import time
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
    except requests.ReadTimeout:
        return None
    if response.status_code == 200:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    urls = selector.css(
        ".tec--list__item article div h3 a::attr(href)"
    ).getall()
    return urls


# Requisito 3
# explicação de requests.exceptions.RequestException obtida em:
# https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
# ela cobrirá exceções de ConnectionError, HTTPError e Timeout.
# Se url_next_page não existe, então uma das exceções será atendida.
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    try:
        url_next_page = selector.css(".tec--btn::attr(href)").get()
    except requests.exceptions.RequestException:
        return None
    return url_next_page


# solução 2 de shares_count
def handle_with_shares_count(shares_count):
    if shares_count == "" or shares_count is None:
        return shares_count == 0

    # outra alternativa para tratar shares_count
    try:
        new_shares_count = shares_count.split()[0]
    except AttributeError:
        print("Erro aconteceu")
    return new_shares_count


# Requisito 4 - feito com a ajuda de Erik Kreis
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("h1.tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = (
        selector.css(".tec--author__info p *::text").get()
        or selector.css(".tec--timestamp__item a::text").get()
    )
    if writer == "" or writer is None:
        writer = None
    if writer is not None:
        writer = writer.strip()

    # solução 1 de shares_count
    # shares_count = selector.css(
    #     "div.tec--toolbar__item::text"
    # ).re_first(r"\d+")

    # solução 2 de shares_count
    shares_count = selector.css("div.tec--toolbar__item::text").get()
    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    summary = selector.css(
        ".tec--article__body > p:first-child *::text"
    ).getall()
    summary = "".join(summary)
    sources = selector.css("div.z--mb-16 h2 ~ div a.tec--badge::text").getall()
    sources = [source.strip() for source in sources]
    categories = selector.css("#js-categories a::text").getall()
    categories = [category.strip() for category in categories]
    # solução 2 de shares_count
    shares_count = handle_with_shares_count(shares_count)
    if comments_count == "" or comments_count is None:
        comments_count = 0

    dictionary = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": int(shares_count),
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }

    return dictionary


# Requisito 5
def get_tech_news(amount):
    URL_BASE = "https://www.tecmundo.com.br/novidades"
    url_accumulator = []

    while len(url_accumulator) < amount:
        html_content = fetch(URL_BASE)
        urls_list_from_titles = scrape_novidades(html_content)
        url_accumulator.extend(urls_list_from_titles)

        if len(url_accumulator) < amount:
            URL_BASE = scrape_next_page_link(html_content)

        if len(url_accumulator) > amount:
            url_accumulator = url_accumulator[:amount]

    news_content_list = [
        scrape_noticia(fetch(url_novidade))
        for url_novidade in url_accumulator
    ]

    create_news(news_content_list)

    return news_content_list
