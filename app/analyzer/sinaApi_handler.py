# !/usr/bin/python
# coding:utf-8
import urllib.request
import urllib.parse
import json
import os


ACCESS_TOKEN = "2.00Pz6y6GQtNpcB9d1129ca42xhgIHD"
URL_PREFIX = "https://api.weibo.com/2/search/topics.json"
CURRENT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/polarity/'
POSITIVE_WORDS_PATH = "positive_words.txt"
NEGATIVE_WORDS_PATH = "negative_words.txt"
POSITIVE_WEIBO_PATH = "positive_weibo.txt"
NEGATIVE_WEIBO_PATH = "negative_weibo.txt"
COUNT = "50"


class SinaAPIRequest:
    def __init__(self):
        with open(CURRENT_DIR_PATH + POSITIVE_WORDS_PATH) as positive_words_doc:
            self.positive_words = list(line.rstrip() for line in positive_words_doc)
        with open(CURRENT_DIR_PATH + NEGATIVE_WORDS_PATH) as negative_words_doc:
            self.negative_words = list(line.rstrip() for line in negative_words_doc)

    def getPolarityWeibo(self, polarity):
        polarity_words = []
        weibo_file = ""
        if polarity == 'positive':
            polarity_words = self.positive_words
            weibo_file = open(CURRENT_DIR_PATH + POSITIVE_WEIBO_PATH, 'w+')
        else:
            polarity_words = self.negative_words
            weibo_file = open(CURRENT_DIR_PATH + NEGATIVE_WEIBO_PATH, 'w+')
        for word in polarity_words:
            topic = urllib.parse.urlencode({'q': word})
            for i in range(1, 5):
                page = str(i)
                url = URL_PREFIX + '?' + topic + '&page=' + page + '&count=' + COUNT + '&access_token=' + ACCESS_TOKEN
                weibo = urllib.request.urlopen(url).read().decode()
                weibo_json = json.loads(weibo)
                rows = 0
                for user in weibo_json['statuses']:
                    rows = rows + 1
                    text = user['text']
                    weibo_file.write(text + '\n')
        weibo_file.close()


def get_microblogs_by_keywords(keyword):
    topic = urllib.parse.urlencode({'q': keyword})
    microblogs = []
    for i in range(1, 5):
        page = str(i)
        url = URL_PREFIX + '?' + topic + '&page=' + page + '&count=' + COUNT + '&access_token=' + ACCESS_TOKEN
        weibo = urllib.request.urlopen(url).read().decode()
        weibo_json = json.loads(weibo)
        rows = 0
        for user in weibo_json['statuses']:
            rows = rows + 1
            text = user['text']
            microblogs.append(text)
    return microblogs

