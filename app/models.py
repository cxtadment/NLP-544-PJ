from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

#polarity: 0 for negative, 1 for positive, 2 for neutral
class Hashtag(db.Document):
    name = db.StringField(required=True, max_length=255)
    polarity = db.IntField(required=True)
    sentiment = db.StringField()


class EmotIcon(db.Document):
    name = db.StringField(required=True, max_length=64)
    url = db.StringField(required=True)
    polarity = db.IntField(required=True)
    sentiment = db.StringField()


class Microblog(db.Document):
    microblogId = db.StringField(required=True)
    text = db.StringField(required=True)
    polarity = db.IntField(required=True)
    sentiment = db.StringField()


class Result(db.Document):
    microblog = db.ReferenceField(Microblog)
    posPercent = db.floatField(required=True)
    negPercent = db.floatField(required=True)
    polarity = db.IntField(required=True)
    sentiment = db.StringField()
