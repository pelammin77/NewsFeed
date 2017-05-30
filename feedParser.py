from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import feedparser
import bs4 as bs
from newspaper import Article
import re, math
from collections import Counter


class Summarizer:
    def __init__(self, min_sum=0.1, max_sum=0.9):
        self._min_sum = min_sum
        self._max_sum = max_sum
        self._stopwords = set(stopwords.words('english') + list(punctuation))



    def _find_common_words(self):
        pass

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
        #print(word_sent.most_common(15))
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










parser = Parser('http://rss.cnn.com/rss/edition.rss')
title, text = parser.get_news()

summary = Summarizer()
print(title)
for s in summary._summarize(text, 1):
    print('* ' + s)
