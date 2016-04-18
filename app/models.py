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


#type: 0 for training, 1 for testing
class Microblog(db.Document):
    microblogId = db.StringField(required=True)
    text = db.StringField(required=True)
    microblogType = db.StringField(required=True)
    polarity = db.StringField(required=True)
    topic  = db.StringField()
    sentiment = db.StringField()
    negCount = db.IntField()
    posCount = db.IntField()
    taggings = db.ListField(db.StringField())
    words = db.ListField(db.StringField())

    def __str__(self):
        return "microblogId: %s, text: %s, polarity: %s, microblogType: %s, topic: %s, sentiment: %s" % (self.microblogId, self.text, self.polarity, self.microblogType, self.topic, self.sentiment)


class Result(db.Document):
    microblog = db.ReferenceField(Microblog)
    posPercent = db.FloatField(required=True)
    negPercent = db.FloatField(required=True)
    polarity = db.IntField(required=True)
    sentiment = db.StringField()

    def __str__(self):
        return "microblogId: %s, posPercent: %s, negPercent: %s, polarity: %s, sentiment: %s" % (self.microblogId, self.posPercent, self.negPercent, self.polarity, self.sentiment)


class TestResult(db.Document):
    classifier = db.StringField()
    accuracy = db.FloatField()
    precision = db.FloatField()
    recall = db.FloatField()
    pos_count = db.IntField()
    neg_count = db.IntField()
    neu_count = db.IntField()
    f_score = db.FloatField()
    pos_precision = db.FloatField()
    pos_recall = db.FloatField()
    pos_f_score = db.FloatField()
    neg_precision = db.FloatField()
    neg_recall = db.FloatField()
    neg_f_score = db.FloatField()
    neu_precision = db.FloatField()
    neu_recall = db.FloatField()
    neu_f_score = db.FloatField()


class SearchResult(db.Document):
    text = db.StringField()
    polarity = db.StringField()
    confidence = db.FloatField()
    words = db.ListField(db.StringField())
    filter_text = db.StringField()

    def serialize(self):
        return {
            'text': self.text,
            'polarity': self.polarity,
            'confidence': self.confidence,
            'words': self.words,
            'filter_text': self.filter_text,
        }


class TestDict(db.Document):
    thisdict = db.DictField()
