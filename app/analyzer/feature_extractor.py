# encoding=utf-8
import jieba
import os
import jieba.posseg as pseg
import re

CURRENT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/'
INPUT_POS_PATH = CURRENT_DIR_PATH + 'sentiment_zh/combinePositive.txt'
INPUT_NEG_PATH = CURRENT_DIR_PATH + 'sentiment_zh/combineNegative.txt'
STOPWORDS_PATH = CURRENT_DIR_PATH + 'segment_filter/chinese_stopwords.txt'
TOPICS_PATH = CURRENT_DIR_PATH + 'segment_filter/topics.txt'
ESCAPE_WORDS = ['不']

class FeatureExtractor:

    def __init__(self):
        with open(INPUT_POS_PATH, 'r') as input_pos_doc:
            self.posDic = set([line.rstrip() for line in input_pos_doc])
        with open(INPUT_NEG_PATH, 'r') as input_neg_doc:
            self.negDic = set([line.rstrip() for line in input_neg_doc])
        with open(STOPWORDS_PATH, 'r') as stopwords_doc:
            self.stopwords = set([line.rstrip() for line in stopwords_doc])
        with open(TOPICS_PATH, 'r') as topics_doc:
            self.topics=set()
            for line in topics_doc:
                segment_list=list(jieba.cut(line.rstrip()))
                for segment in segment_list:
                    self.topics.add(segment)

    """

    use jieba to segment sentence and NTUSD to do the baseline count

    """
    def polarity_count(self, microblog_text):

        seg_list = list(jieba.cut(microblog_text))
        t = 0
        while t < len(seg_list) - 1:
            if seg_list[t] in ESCAPE_WORDS:
                seg_list[t + 1] = seg_list[t] + seg_list[t + 1]
                seg_list.pop(t)
            t += 1

        posCount, negCount = 0, 0
        for word in seg_list:
            if word in self.posDic:
                posCount += 1
            if word in self.negDic:
                negCount += 1

        return posCount, negCount

    """

    filter segment result

    """
    def seg_filter(self, word, tagging):
        # filter stop words including punctuation
        if word in self.stopwords:
            return False
        # filter element containing number
        if re.match('^(?=.*\\d)', word):
            return False
        if word in self.topics:
            return False
        return True

    """

    use jieba to do pos tagging

    """

    def pos_tagging(self, microblog_text):

        words_taggings = pseg.cut(microblog_text)

        words, taggings = [], []
        for word, tagging in words_taggings:
            if self.seg_filter(word, tagging):
                words.append(word)
                taggings.append(tagging)
        return words, taggings






