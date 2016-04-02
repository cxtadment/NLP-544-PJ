#coding=utf-8

from flask.ext.script import Manager, Server
from app import create_app
from app.analyzer.data_handler import hashtag_handler, microblog_handler, emoticon_handler
from app.models import Hashtag, Microblog, Emoticon

app = create_app()
manager = Manager(app)

manager.add_command("runserver", Server(host='0.0.0.0', port=5000, use_debugger=True))

"""

hashtag command operators

"""
@manager.command
def add_hashtag():
    hashtags = hashtag_handler()
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
    emoticons = emoticon_handler()
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
    microblogs = microblog_handler()
    Microblog.objects.insert(microblogs)

@manager.command
def delete_microblog_by_id(microblog_id):
    microblog = Microblog.objects(microblogId=microblog_id).first()
    if microblog:
        microblog.delete()

@manager.command
def delete_all_microblogs():
    Microblog.objects.delete()

@manager.command
def print_microblog():
    print(Microblog.objects)


if __name__ == '__main__':
    manager.run()