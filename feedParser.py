import feedparser
import bs4
from urllib.request import urlopen as uReq

feeds = feedparser.parse('http://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-34837')
print( feeds)

for post in feeds.entries:

    print(post.title + ': '+ post.link + "\n")


