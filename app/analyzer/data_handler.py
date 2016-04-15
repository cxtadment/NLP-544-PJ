# coding=utf-8

from app.models import Hashtag, Emoticon, Microblog
from app.analyzer.data_filter import readWeibo

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
    result = []
    microblogs = readWeibo()
    for polarity in microblogs:
        print(polarity)
        microblog_list = microblogs[polarity]
        for i in range(0, len(microblog_list)):
            microblog = microblog_list[i]
            #do you code here
            if microblog_type == "training":
                single_microblog = Microblog(microblogId=microblog[0], text=microblog[1], polarity=microblog[2],
                                             microblogType=0, topic="", sentiment="")
            elif microblog_type == "testing":
                single_microblog = Microblog(microblogId=microblog[0], text=microblog[1], polarity=microblog[2],
                                             microblogType=1, topic="*ddd", sentiment="dsadas")
            result.append(single_microblog)
    return result

