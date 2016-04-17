# coding=utf-8
from app.analyzer.feature_extractor import FeatureExtractor

from app.models import Hashtag, Emoticon, Microblog
from app.analyzer.data_filter import read_and_filter_data
import os


"""

hashtag data handler

"""


def hashtag_data_handler():
    hashtags = []

    #do you code here
    single_tag = Hashtag(name="das", polarity=1, sentiment="***")
    hashtags.append(single_tag)

    return hashtags


"""

emoticon data handler

"""


def emoticon_data_handler():
    emoticons = []

    #do you code here
    single_emoticon = Emoticon(name="***", url="***", polarity=1, sentiment="***")
    emoticons.append(single_emoticon)

    return emoticons


"""

microblog data handler

"""


def microblog_data_handler(microblog_type):

    microblogs = read_and_filter_data(microblog_type)

    feature_extractor = FeatureExtractor()
    result = []

    for polarity in microblogs:
        microblog_list = microblogs[polarity]
        for microblog in microblog_list:

            #feature extractor
            microblogId, microblog_text, polarity = microblog[0], microblog[1], microblog[2]
            posCount, negCount = feature_extractor.polarity_count(microblog_text)
            words, taggings = feature_extractor.pos_tagging(microblog_text)
            
            single_microblog = Microblog(microblogId=microblogId, text=microblog_text, polarity=polarity, negCount=negCount,
                                         posCount=posCount, words=words, taggings=taggings, microblogType=microblog_type, topic='', sentiment='')
            result.append(single_microblog)

    return result

