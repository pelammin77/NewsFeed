from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import feedparser
import bs4 as bs
#import nltk, re, pprint
#from nltk import word_tokenize
from newspaper import Article
#from urllib.request import urlopen as uReq

class Summarizer:
    def __init__(self, min_sum=0.1, max_sum=0.9):
        self._min_sum = min_sum
        self._max_sum = max_sum
        self._stopwords = set(stopwords.words('finnish') + list(punctuation))

    def _compute_words(self, words):
        pass

    def _summarize(self, text, n):
        pass

    def _rank(self, ranking, n):
        return nlargest(n,ranking, key=ranking.get)







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

    news = feeds.entries[1]
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
    soup = bs.BeautifulSoup(sauce, 'html.parser')
   # text = soup.find_all('p')
    #text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    #print(text)
    parseNews(soup,MTV3_ARTICLE_CLASS)
    #parseMTV3(soup)
    #print(soup.find_all('p'))
   # print(soup.title.text)



#    print(soup.get_text())


def article_tokenizer():
    post_text = feedparser.parse('http://www.mtv.fi/api/feed/rss/uutiset_uusimmat')
    post_text['feed']['titlr']







def parseMTV3(soup):
   # soup.find('p', attrs={'class': 'lead'})
    article = soup.findAll('p',"div", {"class": MTV3_ARTICLE_CLASS})

    print(article)
    #for para in article:
       # print(para.string)
      # print(para.string)

def parseYLE(soup):
    article = soup.findAll("div", {"class": YLE_ARTICLE_CLASS})
   # print(article)
    for para in article:
        print(para.text)

def parseNews(soup,articleClass):
    [s.extract() for s in soup('style')]
    article = soup.findAll("div",  {"class": articleClass}, "p")
    # print(article)
    for para in article:
        print(para)



parseFeed()
#print('Article title: ' + title)
# print(authors)

