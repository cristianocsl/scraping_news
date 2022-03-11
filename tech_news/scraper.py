from parsel import Selector
import requests
import time


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
    except requests.ReadTimeout:
        return None
    if response.status_code != 200:
        return None
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
        url_next_page = selector.css(
            ".tec--btn::attr(href)"
        ).get()
    except requests.exceptions.RequestException:
        return None
    return url_next_page


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
