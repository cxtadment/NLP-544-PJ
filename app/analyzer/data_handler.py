#coding=utf-8

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
def microblog_data_handler(microblog_type):

    microblogs = []

    #do you code here
    if microblog_type == "training":
        single_microblog = Microblog(microblogId="***", text="***", polarity=1, microblogType=0, topic="***", sentiment="***")
    elif microblog_type == "testing":
        single_microblog = Microblog(microblogId="233", text="dasdas", polarity=1, microblogType=1, topic="*ddd", sentiment="dsadas")

    microblogs.append(single_microblog)

    return microblogs

