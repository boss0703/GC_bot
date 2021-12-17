import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import chromedriver_binary

from config import EPIC_NEWS_URL, GAME_NEWS_URL, GAME_NEWS_URL_HEAD, FX_NEWS_URL, FX_INFO_URL, BABY_NEWS_URL, BABY_NEWS_URL_HEAD, \
    BABY_NEWS_LIMIT, GAME_NEWS_LIMIT, FX_NEWS_LIMIT, FX_INFO_LIMIT


def main():
    # game_news()
    # fx_info()
    # baby_news()
    return


def game_news():
    session = requests.session()
    response = session.get(GAME_NEWS_URL)
    bs = BeautifulSoup(response.text, 'html.parser')
    # 記事タイトル
    bstitle = bs.select('section.item--normal .figcaption .title', limit=GAME_NEWS_LIMIT)
    titles = []
    for s in bstitle:
        titles.append(s.text)
    # 記事のURL
    bsurl = bs.select('section.item--normal a.link', limit=GAME_NEWS_LIMIT)
    urls = []
    for s in bsurl:
        urls.append(GAME_NEWS_URL_HEAD + s.get('href'))

    res = ''
    for (title, url) in zip(titles, urls):
        res += '[' + title + '](' + url + ')\n\n'
    print('successfully game news scraping')
    return res


def fx_news():
    session = requests.session()
    response = session.get(FX_NEWS_URL)
    bs = BeautifulSoup(response.text, 'html.parser')

    # 記事タイトル
    bstitle = bs.select('#ytopContentIn h3.yjL.marB6,#ytopContentIn span.dtl', limit=FX_NEWS_LIMIT)
    titles = []
    for s in bstitle:
        titles.append(s.text)

    # 記事のURL
    bsurl = bs.select('#ytopContentIn a', limit=FX_NEWS_LIMIT)
    urls = []
    for s in bsurl:
        urls.append(s.get('href'))

    res = ''
    for (title, url) in zip(titles, urls):
        res += '[' + title + '](' + url + ')\n\n'
    print('successfully fx news scraping')
    return res


def fx_info():
    session = requests.session()
    response = session.get(FX_INFO_URL)
    bs = BeautifulSoup(response.text, 'html.parser')

    # 記事タイトル
    bstd = bs.select('div#main div.ecoEventTbl02.marB20 '
                     'tr:has(td span.icoEu18,.icoUsa18,.icoAus18,.icoMxn18,.icoGer18,.icoFra18,.icoGbr18),'
                     'div#main div.ecoEventTbl02.marB20 tr th.date', limit=FX_INFO_LIMIT)
    date = ''
    res_arr = []
    for td in bstd:
        # 日付の場合
        if re.compile(r'\d{1,2}/\d{1,2}.*').search(td.text):
            date = td.text.strip("\n")
        # それ以外の場合
        else:
            td_arr = td.text.strip("\n").splitlines()
            # 数値が無い系の情報の場合
            if len(td_arr) < 3:
                td_arr.append('')
            # 日付をつける
            td_arr[0] = date + ' ' + td_arr[0]
            # 3番目の情報に国名を入れる
            if 'icoUsa18' in str(td):
                td_arr[2] = 'USA'
            elif 'icoEu18' in str(td):
                td_arr[2] = 'EU'
            elif 'icoAus18' in str(td):
                td_arr[2] = 'AUS'
            elif 'icoMxn18' in str(td):
                td_arr[2] = 'MXN'
            elif 'icoGer18' in str(td):
                td_arr[2] = 'GER'
            elif 'icoFra18' in str(td):
                td_arr[2] = 'FRA'
            elif 'icoGbr18' in str(td):
                td_arr[2] = 'GBR'
            else:
                td_arr[2] = 'NON'
            res_arr.append(td_arr)
    res = ''
    for arr in res_arr:
        res += " ".join([str(i) for i in arr])
        res += '\n'
    return res


def baby_news():
    session = requests.session()
    response = session.get(BABY_NEWS_URL)
    bs = BeautifulSoup(response.text, 'html.parser')

    # 記事タイトル
    bstitle = bs.select('.thm-main h3.title', limit=BABY_NEWS_LIMIT)
    titles = []
    for s in bstitle:
        titles.append(s.text)

    # 記事のURL
    bsurl = bs.select('.thm-main div.news-list section a', limit=BABY_NEWS_LIMIT)
    urls = []
    for s in bsurl:
        urls.append(BABY_NEWS_URL_HEAD + s.get('href'))

    res = ''
    for (title, url) in zip(titles, urls):
        res += '[' + title + '](' + url + ')\n\n'
    print('successfully baby news scraping')
    return res


def epic_news():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(EPIC_NEWS_URL)
    time.sleep(1)

    html = driver.page_source

    bs = BeautifulSoup(html, 'html.parser')

    bstitle = bs.select('main > div.css-1ktypff > div > div > div > div > div:nth-child(2) > span > div > div > section > div > div:not(:last-child) > div > div > a > div > div > div.css-hkjq8i > span.css-2ucwu > div')
    print(bstitle)
    res = ''
    for s in bstitle:
        res += '・' + s.text + '\n'
    print('successfully epic news scraping')
    return res

if __name__ == "__main__":
    main()
