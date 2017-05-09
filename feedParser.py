import feedparser
import bs4
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
    authors = article.authors
    title =  article.title
    date = article.publish_date
   # print(article.text)



parseFeed() #Toimii

print(title)
print(authors)