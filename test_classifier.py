import sentiment_module as s

print(s.sentiment("this is good news"))
print(s.sentiment("this is bad news"))
print(s.sentiment("End of the world is cumming"))
print(s.sentiment("I am ill and i do not have any money I kill myself"))
print(s.sentiment("python and nltk are great "))

posNews = """ Sea Cow Population Thriving in Australia Thanks to Baby Boom
In 2011, the dugong population of the Great Barrier Reef was estimated to be 600 without any sign of calves
or newborns – the lowest it had been since the 1980s. The condition of the species, categorized as 
“vulnerable to extinction”, caused great alarm amongst conservationists.

Half a decade later, however, sea cows have rebounded to about 5,000 in number – 10% of which are calves,
 according to aerial surveys conducted off the east coast of Queensland.
This exciting comeback can be credited to the return of sea grass to the region; the main component of a
sea cow’s diet. Most of the sea grass near the Great Barrier Reef was wiped out due to the effects of Cyclone Yasi."""

print(s.sentiment(posNews))