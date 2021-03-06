# coding=utf-8
from app.analyzer.data_filter import DataFilter
from app.analyzer.feature_extractor import FeatureExtractor
from app.analyzer.sinaApi_handler import get_microblogs_by_keywords

from app.models import Hashtag, Emoticon, Microblog


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

    data_filter = DataFilter()
    microblogs_text = get_microblogs_by_keywords(keyword)

    feature_extractor = FeatureExtractor()
    result = []
    for text in microblogs_text:
        filter_text = data_filter.text_filters(text)
        words, taggings = feature_extractor.pos_tagging(filter_text)
        result.append((text, filter_text, words, taggings))

    return result


def microblog_data_handler(microblog_type):

    data_filter = DataFilter()
    microblogs = data_filter.read_and_filter_api_microblog_data(microblog_type)

    result = []

    feature_extractor = FeatureExtractor()
    for polarity in microblogs:
        microblog_list = microblogs[polarity]
        for microblog in microblog_list:

            #feature extractor
            microblogId, microblog_raw_text, microblog_text, polarity = microblog[0], microblog[1], microblog[2],  microblog[3]
            posCount, negCount = feature_extractor.polarity_count(microblog_text)
            words, taggings = feature_extractor.pos_tagging(microblog_text)
            raw_words, raw_taggings = feature_extractor.pos_tagging(microblog_raw_text)

            single_microblog = Microblog(microblogId=microblogId, text=microblog_text, polarity=polarity, microblogType=microblog_type, topic='',
                                         posCount=posCount, negCount=negCount, words=words, taggings=taggings,
                                         raw_words=raw_words, raw_taggings=raw_taggings, sentiment='')

            result.append(single_microblog)

    return result

