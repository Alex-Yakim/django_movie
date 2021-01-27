from django.core.management.base import BaseCommand

import requests
import threading
from bs4 import BeautifulSoup as BS
from rk_parser.models import Product

# start_page = "https://www.rusklimat.ru/ekaterinburg/uvlazhniteli-i-ochistiteli-vozdukha/uvlazhniteli-vozdukha/"
urls = []
item_url = []
soups = []
HOST = 'https://www.rusklimat.ru'


# расчет количества страниц
def pages_count(html):
    r = requests.get(html, params=None)
    page_bs = BS(r.content, 'html.parser')
    pagination = page_bs.select('div.paginator > ul > li > a')
    if pagination:
        return int(pagination[-1].string)
    else:
        return 1


# запрос всех страниц в каталоге
def get_urls(start_page):
    print('Начало парсинга')
    for x in range(1, pages_count(start_page) + 1):
        urls.append(requests.get(start_page + 'page-' + str(x)))
    else:
        print('Urls - ' + str(len(urls)))


# поиск всех товаров
def get_item_url():
    for u in urls:
        page_bs = BS(u.content, 'html.parser')
        for i in page_bs.select('#catalog_items > .item.b-line > div.w > div.ttl > a'):
            item_url.append(HOST + i.get('href'))
    print('Товаров - ' + str(len(item_url)))


# парсинг товаров
def item_parse(url):
    # print(f'Парсинг товара {item_url.index(i) + 1} из {len(item_url)}')
    r = requests.get(url)
    soup = BS(r.content, 'html.parser')
    name = soup.select('h1.ttl.element__header')[0].string  # Получение названия
    article = soup.select('div.article > span.textspan > b')[0].string  # Получение артикула
    # price = soup.select('div.prices > div.price')[0].string.strip()  # Получение цены
    div_prices = soup.select('div.prices')
    price = div_prices[0].div.string.strip()
    p = Product(
        name=name,
        article=article,
        price=price.replace(' р.', ''),
        url=url
    ).save()
    print(f'Товар {name}')


class Command(BaseCommand):
    help = 'Парсинг русклимат'

    def add_arguments(self, parser):
        parser.add_argument('start_page', nargs='+')

    def handle(self, *args, **options):
        for page in options['start_page']:
            get_urls(page)
        get_item_url()
        thread_list = []
        for i in range(len(item_url)):
            t = threading.Thread(target=item_parse, args=(item_url[i],))
            thread_list.append(t)
            t.start()
        for t in thread_list:
            t.join()
