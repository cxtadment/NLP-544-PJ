# coding=utf-8
from app.analyzer.feature_extractor import FeatureExtractor
from app.analyzer.sinaApi_handler import get_microblogs_by_keywords

from app.models import Hashtag, Emoticon, Microblog

from app.analyzer.data_filter import text_filters, read_and_filter_api_microblog_data, read_and_filter_data
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


def api_microblog_data_handler(keyword):

    microblogs_text = get_microblogs_by_keywords(keyword)

    feature_extractor = FeatureExtractor()
    result = []
    for text in microblogs_text:
        filter_text = text_filters(text)
        words, taggings = feature_extractor.pos_tagging(filter_text)
        result.append((text, filter_text, words, taggings))

    return result



def microblog_data_handler(microblog_type):

    microblogs = read_and_filter_data(microblog_type)
    # microblogs = read_and_filter_api_microblog_data(microblog_type)
    result = []

    feature_extractor = FeatureExtractor()
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

