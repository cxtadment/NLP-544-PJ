#coding=utf-8
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

#polarity: 0 for negative, 1 for positive, 2 for neutral
class Hashtag(db.Document):
    name = db.StringField(required=True, max_length=255)
    polarity = db.IntField(required=True)
    sentiment = db.StringField()

    def __str__(self):
        return "name: %s, polarity: %s, sentiment: %s" % (self.name, self.polarity, self.sentiment)


class Emoticon(db.Document):
    name = db.StringField(required=True, max_length=64)
    url = db.StringField(required=True)
    polarity = db.IntField(required=True)
    sentiment = db.StringField()

    def __str__(self):
        return "name: %s, url: %s, polarity: %s, sentiment: %s" % (self.name, self.url, self.polarity, self.sentiment)


class Microblog(db.Document):
    microblogId = db.StringField(required=True)
    text = db.StringField(required=True)
    polarity = db.IntField(required=True)
    sentiment = db.StringField()

    def __str__(self):
        return "microblogId: %s, text: %s, polarity: %s, sentiment: %s" % (self.microblogId, self.text, self.polarity, self.sentiment)


class Result(db.Document):
    microblog = db.ReferenceField(Microblog)
    posPercent = db.FloatField(required=True)
    negPercent = db.FloatField(required=True)
    polarity = db.IntField(required=True)
    sentiment = db.StringField()

    def __str__(self):
        return "microblogId: %s, posPercent: %s, negPercent: %s, polarity: %s, sentiment: %s" % (self.microblogId, self.posPercent, self.negPercent, self.polarity, self.sentiment)
