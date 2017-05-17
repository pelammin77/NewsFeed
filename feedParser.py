from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import feedparser
import bs4 as bs
from newspaper import Article


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

        text = text.strip()
        sents = sent_tokenize(text)
        assert n <= len(sents)
        print(len(sents))
        print(sents)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_words(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)

        return [sents[j] for j in sents_idx]

    def _rank(self, ranking, n):
        r = nlargest(n, ranking, key=ranking.get)
        # print(r)
        return r

'''
MTV3_ARTICLE_CLASS = 'editorial'
YLE_ARTICLE_CLASS = 'yle__article__content'
authors = ""
title = ""
date = ""
'''

class Parser:
    def __init__(self, link):
        self._link = link
        #self.title = ""


    def parse_feed(self):
        self._feeds = feedparser.parse(self._link)



    def make_soup(self, soup):
        pass


    def parse_news(self, soup):
        pass

def parseFeed():
    feeds = feedparser.parse('http://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET')
    #feeds = feedparser.parse('http://www.mtv.fi/api/feed/rss/uutiset_uusimmat')
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
    make_soup(sauce)


def make_soup(sauce):
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    parseNews(soup)

def article_tokenizer():
    post_text = feedparser.parse('http://www.mtv.fi/api/feed/rss/uutiset_uusimmat')
    post_text['feed']['title']


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


def parseNews(soup):
    # news = ""
    [s.extract() for s in soup('style')]
    [s.extract() for s in soup('a')]
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    summary = Summarizer()
    for s in summary._summarize(text, 5):
        print('* ' + s)


parseFeed()
# print('Article title: ' + title)
# print(authors)
