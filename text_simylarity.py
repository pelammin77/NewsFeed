"""
file: text simylarity.py
author: Petri Lamminaho 



"""

import re, math
from collections import Counter
import nltk


WRD = re.compile(r'\w+')

# calculates two vectors similarity (cosine similarity)
def get_cos(vect1, vect2):
    inter = set(vect1.keys())& set(vect2.keys())
    num = sum([vect1[x] * vect2[x] for x in inter])

    sum1 = sum([vect1[x]**2 for x in vect1.keys()])
    sum2 = sum([vect2[x]**2 for x in vect2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        0.0
    else:
        return float(num)/ denominator

# converts text to vector
def text_to_vector(text):
    words = WRD.findall(text)
    return Counter(words)

# Gets sen post tag
def get_tags(sen, tag='NNP'):

    tagged_sent = nltk.pos_tag(sen.split())
    propernouns = [word for word, pos in tagged_sent if pos == tag]
    print(propernouns)


def search_text(key_text, seach_line):
    seach_result = re.search(key_text, seach_line, re.M|re.I)
    if seach_result:
        print("Text " + seach_result.group() + " found")
    else:
        print("Text not found")



# Test/main
text1 = "White House communications director quits"
text2 = 'White House communications director Mike Dubke is leaving the administration, ' \
        'he said Tuesday, amid swirling speculation about a possible Trump staff shakeup.'
text3 = 'Putin meets Trump'
text4 = 'Trump meets Putin'
text5 = 'Trump is Russian spy'

vector1 = text_to_vector(text3)
vector2 = text_to_vector(text4)

cosine = get_cos(vector1, vector2)




print('cosine', cosine)
get_tags(text1)
get_tags(text2)
