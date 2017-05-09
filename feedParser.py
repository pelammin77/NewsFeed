import feedparser
import bs4 as bs
from newspaper import Article

import bs4
from urllib.request import urlopen as uReq
#http://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET
authors = ""
title = ""
date = ""

def parseFeed():
    feeds = feedparser.parse('http://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET')
    for post in feeds.entries:
      print("")
       #print(post.title + ': ' + post.link + "\n")

    news = feeds.entries[0]
    print(news.link)
    parseArticle(news.link)

def parseArticle(url):
    global authors
    global date
    global title

    article = Article(url)
    article.download()
    article.parse()
    sauce= article.html
    authors = article.authors
    title = article.title
    date = article.publish_date
    #print(article.text)
    #print(article.summary)
   # len(article.summary)
    make_soup(sauce)

def make_soup(sauce):
    soup = bs.BeautifulSoup(sauce, 'lxml')
    #print(soup.find_all('p'))
   # print(soup.title.text)

    for para in soup.find_all('p'):
        print(para.text + '\n')
#    print(soup.get_text())


parseFeed()
print('Article title: ' + title)
# print(authors)

