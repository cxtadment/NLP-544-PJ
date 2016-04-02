#coding=utf-8

from app.models import Hashtag, Emoticon

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
def microblog_data_handler(type):

    microblogs = []

    #do you code here
    if type == "training":
        single_microblog = Hashtag(microblogId="***", text="***", polarity=1, type=0, topic="***", sentiment="***")
    else:
        single_microblog = Hashtag(microblogId="***", text="***", polarity=1, type=1, topic="***", sentiment="***")

    microblogs.append(single_microblog)

    return microblogs

