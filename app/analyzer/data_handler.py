#coding=utf-8

from app.models import Hashtag, Emoticon


def hashtag_handler():

    hashtags = []

    #do you code here
    single_tag = Hashtag(name="das", polarity=1, sentiment="***")
    hashtags.append(single_tag)

    return hashtags


def emoticon_handler():

    emoticons = []

    #do you code here
    single_emoticon = Emoticon(name="***", url="***", polarity=1, sentiment="***")
    emoticons.append(single_emoticon)

    return emoticons


def microblog_handler():

    microblogs = []

    #do you code here
    single_microblog = Hashtag(microblogId="***", text="***", polarity=1, sentiment="***")
    microblogs.append(single_microblog)

    return microblogs

