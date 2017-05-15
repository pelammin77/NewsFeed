from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import feedparser
import bs4 as bs
# import nltk, re, pprint
# from nltk import word_tokenize
from newspaper import Article


# from urllib.request import urlopen as uReq

class Summarizer:
    def __init__(self, min_sum=0.1, max_sum=0.9):
        self._min_sum = min_sum
        self._max_sum = max_sum
        self._stopwords = set(stopwords.words('finnish') + list(punctuation))

    def _compute_words(self, words_sen):
        freq = defaultdict(int)

        for sen in words_sen:
            for word in sen:
                if word not in self._stopwords:
                    freq[word] += 1
        m = float(max(freq.values()))
        for w in freq.copy().keys():
            freq[w] = freq[w] / m
            if freq[w] >= self._max_sum or freq[w] <= self._min_sum:
                del freq[w]
        return freq

    def _summarize(self, text, n):
        # print("Luokka tulostaa" + text)
        sents = sent_tokenize(text)
        print(sents)
        assert n <= len(sents)
        #words = [word_tokenize(s.lower)for s in sents]
        words = word_tokenize(text)
        print(words)
        self._freq = self._compute_words(words)
        ranking = defaultdict(int)
        for i, sent in enumerate(words):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_ids = self._rank(ranking, n)
        #print(len(sents))
        #print( sents_ids[0])
        for j in sents_ids:
            print(j)
        print(sents[0])

        #return [sents[j] for j in sents_ids]

    def _rank(self, ranking, n):
        return nlargest(n, ranking, key=ranking.get)


MTV3_ARTICLE_CLASS = 'editorial'
YLE_ARTICLE_CLASS = 'yle__article__content'
authors = ""
title = ""
date = ""


def parseFeed():
    # feeds = feedparser.parse('http://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET')
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
    sauce = article.html
    authors = article.authors
    title = article.title
    date = article.publish_date

    # print(article.text)
    # print(article.summary)
    # len(article.summary)
    make_soup(sauce)


def make_soup(sauce):
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    # text = soup.find_all('p')
    # text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    # print(text)
    parseNews(soup, MTV3_ARTICLE_CLASS)
    # parseMTV3(soup)
    # print(soup.find_all('p'))
    # print(soup.title.text)


#    print(soup.get_text())


def article_tokenizer():
    post_text = feedparser.parse('http://www.mtv.fi/api/feed/rss/uutiset_uusimmat')
    post_text['feed']['titlr']


def parseMTV3(soup):
    # soup.find('p', attrs={'class': 'lead'})
    article = soup.findAll('p', "div", {"class": MTV3_ARTICLE_CLASS})

    print(article)
    # for para in article:
    # print(para.string)
    # print(para.string)


def parseYLE(soup):
    article = soup.findAll("div", {"class": YLE_ARTICLE_CLASS})
    # print(article)
    for para in article:
        print(para.text)


def parseNews(soup, articleClass):
    news = ""
    [s.extract() for s in soup('style')]
    article = soup.findAll("div", {"class": articleClass}, "p")
    # print(article)
    for para in article:
        news = news + para.text
        # print(para.text)

    # print(news)

    summary = Summarizer()
    summary._summarize(news, 2)


parseFeed()
# print('Article title: ' + title)
# print(authors)
