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
        self.__link = link
        self._text =""
        self._title= ""



    def __parse_feed(self):
        self._feeds = feedparser.parse(self.__link)
        news = self._feeds.entries[1]
        print(news.link)
       # parseArticle(news.link)

        article = Article(news.link)
        article.download()
        article.parse()
        self._sauce = article.html
        self._authors = article.authors
        self._title = article.title
        self._publish_date = article.publish_date
        self.__make_soup()

    def __make_soup(self): # private
        self.__soup = bs.BeautifulSoup(self._sauce, 'html.parser')
        self.__parse_news()

    def __parse_news(self): # private

        [s.extract() for s in self.__soup('style')]
        [s.extract() for s in self.__soup('a')]
        self._title = self.__soup.find('title').text
        self._text = ' '.join(map(lambda p: p.text, self.__soup.find_all('p')))

    def get_news(self):
        self.__parse_feed()
        return self._title, self._text









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


def parseNews(soup):
    # news = ""
    [s.extract() for s in soup('style')]
    [s.extract() for s in soup('a')]
    title = soup.find('title').text
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    summary = Summarizer()
    print(title)
    for s in summary._summarize(text, 3):
        print('* ' + s)


#parseFeed()
# print('Article title: ' + title)
# print(authors)

parser = Parser('http://www.mtv.fi/api/feed/rss/uutiset_uusimmat')
title, text = parser.get_news()
summary = Summarizer()
print(title)
for s in summary._summarize(text, 3):
    print('* ' + s)
