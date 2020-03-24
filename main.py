
# coding: UTF-8

# 要件
# - 検索ワード，記事タイトル, URLをcsvで出力する
# - 件数を取得してページ数を計算，ページを追ってスクレイピングする

import requests
import csv
from bs4 import BeautifulSoup

# ----------------------------
target_url = 'https://qiita.com/search?'
sort_param = 'like'
# ----------------------------


class Article:
    def __init__(self, title, url, search_keyword):
        self.title = title
        self.url = url
        self.search_keyword = search_keyword


def main():
    # 入力を半角スペース区切りで受け付ける
    keywords = input().split(' ')
    query = make_query(keywords)
    url = "{0}&q={1}".format(target_url, query)
    page_count = get_page_count(url)
    articles = []
    for i in range(page_count):
        page_num = i + 1
        request_url = "{0}&page={1}&q={2}&sort={3}".format(target_url, page_num, query, sort_param)
        articles += do_request(request_url, query)
    write_csv(articles)
    print('Program Finished')


def get_page_count(request_url):
    r = requests.get(request_url)
    soup = BeautifulSoup(r.text, 'lxml')
    article_count = int(soup.body.find(class_='active').find(class_='badge').text)
    return (article_count + 10 - 1) // 10


def make_query(keywords):
    ret = ''
    for i in range(0, len(keywords)):
        if i:
            ret += '+'
        ret += '"' + keywords[i] + '"'
    return ret


def do_request(request_url, query):
    articles = []
    r = requests.get(request_url)
    soup = BeautifulSoup(r.text, 'lxml')
    # 記事タイトルとURLを獲得し，Articleオブジェクトに保存，配列に格納する
    sps = soup.body.find(class_='searchResultContainer_main').find_all(class_='searchResult_itemTitle')
    for sp in sps:
        title = sp.text
        url = 'https://qiita.com/' + sp.a.get('href')
        article = Article(title, url, query)
        articles.append(article)

    return articles


def write_csv(articles):
    with open('data/search_result.csv', 'w') as f:
        writer = csv.writer(f)
        for ac in articles:
            writer.writerow([ac.search_keyword, ac.title, ac.url])


if __name__ == "__main__":
    main()
