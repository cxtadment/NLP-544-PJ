#coding=utf-8

from flask.ext.script import Manager, Server
from app import create_app
from app.analyzer.classifiers.classifier_handler import module_build, classify_testing
from app.analyzer.data_handler import hashtag_data_handler, microblog_data_handler, emoticon_data_handler
from app.analyzer.feature_extractor import FeatureExtractor
from app.models import Hashtag, Microblog, Emoticon, TestDict, TestResult
from app.analyzer.sinaApi_handler import SinaAPIRequest

app = create_app()
manager = Manager(app)

manager.add_command("runserver", Server(host='0.0.0.0', port=5000, use_debugger=True))

"""

hashtag command operators

"""
@manager.command
def add_hashtag():
    hashtags = hashtag_data_handler()
    Hashtag.objects.insert(hashtags)

@manager.command
def delete_hashtag_by_name(hashtag_name):
    hashtag = Hashtag.objects(name=hashtag_name).first()
    if hashtag:
        hashtag.delete()

@manager.command
def delete_all_hashtags():
    Hashtag.objects.delete()

@manager.command
def print_hashtag():
    print(Hashtag.objects)


"""

emoticon command operators

"""

@manager.command
def add_emoticon():
    emoticons = emoticon_data_handler()
    Emoticon.objects.insert(emoticons)

@manager.command
def delete_emoticon_by_name(emoticon_name):
    emoticon = Emoticon.objects(name=emoticon_name).first()
    if emoticon:
        emoticon.delete()

@manager.command
def delete_all_emoticons():
    Emoticon.objects.delete()

@manager.command
def print_emoticon():
    print(Emoticon.objects)


"""

microblog command operators

"""
@manager.command

def add_microblog():
    Microblog.objects.delete()
    microblogs = microblog_data_handler('training')
    print(len(microblogs))
    # Microblog.objects.insert(microblogs)
    # microblogs = microblog_data_handler('testing')
    # print(len(microblogs))
    Microblog.objects.insert(microblogs)

@manager.command
def complete_microblog():
    microblogs = Microblog.objects(microblogType='training')
    print(len(microblogs))
    # new_microblogs = []
    # for microblog in microblogs:
    #     newone = Microblog(microblogId=microblog.microblogId, text=microblog.text, polarity=microblog.polarity, negCount=microblog.negCount,
    #                          posCount=microblog.posCount, words=microblog.words, taggings=microblog.taggings, microblogType=microblog.microblogType, topic='', sentiment='')
    #     new_microblogs.append(newone)
    # Microblog.objects.insert(new_microblogs)


@manager.command
def delete_microblog_by_id(microblog_id):
    microblog = Microblog.objects(microblogId=microblog_id).first()
    if microblog:
        microblog.delete()

@manager.command
def delete_all_microblogs_by_type(microblog_type):
    microblogs = Microblog.objects(microblogType=microblog_type)
    if microblogs:
        microblogs.delete()

@manager.command
def delete_all_microblogs():
    Microblog.objects.delete()

@manager.command
def print_microblog():
    print(len(Microblog.objects))


@manager.command
def test_classifier():
    module_build()
    TestResult.objects.delete()
    classify_testing()

@manager.command
def test_dict():
    thisjson = {"haha": "shabi", "xixi": "caonima"}
    thisdict = TestDict(thisdict=thisjson)
    thisdict.save()
@manager.command
def test_count():
    feature_extracter = FeatureExtractor()
    feature_extracter.polarity_count("我不是不喜欢你，只是不想和你在一起")

@manager.command
def test_feature():
    microblogId, microblog_text, polarity = "234", "我不喜欢你， 你这个愚昧的家伙，脑子有毛病", 1
    feature_extracter = FeatureExtractor()
    words, taggings = feature_extracter.pos_tagging(microblog_text)
    posCount, negCount = feature_extracter.polarity_count(microblog_text)
    single_microblog = Microblog(microblogId=microblogId, text=microblog_text, polarity=polarity, negCount=negCount,
                                             posCount=posCount, words=words, taggings=taggings, microblogType=1, topic=None, sentiment=None)
    single_microblog.save()

@manager.command    
def test_api(polarity):
    api_handler = SinaAPIRequest()
    api_handler.getPolarityWeibo(polarity)

if __name__ == '__main__':
    manager.run()