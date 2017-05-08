import feedparser
from newspaper import Article

import bs4
from urllib.request import urlopen as uReq



def parseFeed():
    feeds = feedparser.parse('http://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-34837')
    for post in feeds.entries:
      print("")
      # print(post.title + ': ' + post.link + "\n")

    news = feeds.entries[0]
    print(news.link)
    parseArticle(news.link)

def parseArticle(url):
    article = Article(url)
    article.download()
    article.parse()
    #print (article.html)
    print(article.title)
    print(article.text)
     


parseFeed() #Toimii

