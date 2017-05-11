import feedparser
import bs4 as bs
from newspaper import Article
#from urllib.request import urlopen as uReq

MTV3_ARTICLE_CLASS = 'editorial'
YLE_ARTICLE_CLASS = 'yle__article__content'
authors = ""
title = ""
date = ""

def parseFeed():
    #feeds = feedparser.parse('http://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET')
    feeds = feedparser.parse('http://www.mtv.fi/api/feed/rss/uutiset_uusimmat')
    for post in feeds.entries:
      print("")
      # print(post.title + ': ' + post.link + "\n")

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


   # print(article.text)
    #print(article.summary)
   # len(article.summary)
    make_soup(sauce)

def make_soup(sauce):
    soup = bs.BeautifulSoup(sauce, 'lxml')
    parseNews(soup,MTV3_ARTICLE_CLASS)
    #print(soup.find_all('p'))
   # print(soup.title.text)



#    print(soup.get_text())







def parseMTV3(soup):
    article = soup.findAll("div", {"class": MTV3_ARTICLE_CLASS})
    for para in article:
       #print(para.text)
       print(para.text)

def parseYLE(soup):
    article = soup.findAll("div", {"class": YLE_ARTICLE_CLASS})
   # print(article)
    for para in article:
        print(para.text)

def parseNews(soup,articleClass):
    article = soup.findAll("div", {"class": articleClass})
    # print(article)
    for para in article:
        print(para.text)



parseFeed()
print('Article title: ' + title)
# print(authors)

