# encoding=utf-8
import jieba
import os
import jieba.posseg as pseg

CURRENT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/sentiment_zh/'
INPUT_POS_PATH = CURRENT_DIR_PATH + 'combinePositive.txt'
INPUT_NEG_PATH = CURRENT_DIR_PATH + 'combineNegative.txt'
ESCAPE_WORDS = ['不']

class FeatureExtractor:

    def __init__(self):
        with open(INPUT_POS_PATH, 'r') as input_pos_doc:
            self.posDic = set([line.rstrip() for line in input_pos_doc])
        with open(INPUT_NEG_PATH, 'r') as input_neg_doc:
            self.negDic = set([line.rstrip() for line in input_neg_doc])

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

    use jieba to do pos tagging

    """

    def pos_tagging(self, microblog_text):

        words_taggings = pseg.cut(microblog_text)

        words, taggings = [], []
        for word, tagging in words_taggings:
            words.append(word)
            taggings.append(tagging)

        return words, taggings
