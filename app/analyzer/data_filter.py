#!/usr/bin/python
# coding:utf-8
import re
import os


TRAINING_INPUT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/data/SIGHAN8-Task2-Corpus-Release/'
TESTING_INPUT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/data/SIGHAN8-Task2-Corpus/'
CURRENT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/polarity/'
POSITIVE_WEIBO_TRAINING_PATH = "positive_weibo_training.txt"
NEGATIVE_WEIBO_TRAINING_PATH = "negative_weibo_training.txt"
NEUTRAL_WEIBO_TRAINING_PATH = "neutral_weibo_training.txt"
POSITIVE_WEIBO_TEST_PATH = "positive_weibo_test.txt"
NEGATIVE_WEIBO_TEST_PATH = "negative_weibo_test.txt"
NEUTRAL_WEIBO_TEST_PATH = "neutral_weibo_test.txt"


class DataFilter:

    def __init__(self):
        self.extra_features = []

    def convertPun(self, content):
        punctuation_list = ['，', '。', '？', '！', '……', ':', '「', '」', '.....', '】', '：', '、']
        punctuation_list2 = ['《', '》', '“', '”', '"', '"']
        for i in range(0, len(punctuation_list)):
            content = content.replace(punctuation_list[i], '.')
            content = content.replace('【', ' ')
        for i in range(0, len(punctuation_list2)):
            content = content.replace(punctuation_list2[i], '')
        return content


    # remove http link
    def removeLink(self, content):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        for i in range(0, len(urls)):
            content = content.replace(urls[i], '')
        return content


    # remove topic including chinese
    def removeTopic(self, content):
        topics = re.findall(u"#[\w\u0000-\u9FFF]+#", content)
        for i in range(0, len(topics)):
            content = content.replace(topics[i], '')
        return content


    # remove content in (), like
    def removeBracket(self, content):
        content = content.replace('（', '(')
        content = content.replace('）', ')')
        brackets = re.findall(u"\([\w\u0000-\u9FFF]+\)", content)
        for i in range(0, len(brackets)):
            content = content.replace(brackets[i], '')
        return content


    # remove private messages
    def removePrivate(self, content):
        privates = re.findall(u"@[\w\u0000-\u9FFF]+", content)
        for i in range(0, len(privates)):
            content = content.replace(privates[i], '')
        return content


    # remove forwarded messages
    def removeForward(self, content):
        forward_index = content.find("//")
        if not forward_index == -1:
            content = content[0:forward_index]
        return content

    def read_annotation_data(self, input_path):

        with open(input_path, 'r') as annotation_file:
            pos_list, neg_list = [], []
            for line in annotation_file:
                line = line.rstrip()
                line_list = line.split('	')
                wid, num = line_list[3], line_list[4]
                if num == '1':
                    pos_list.append(wid)
                elif num == '-1':
                    neg_list.append(wid)

            return pos_list, neg_list

    def text_filters(self, weibo_content):

        weibo_content = weibo_content.replace(' ', '')
        weibo_content = self.removeLink(weibo_content)
        weibo_content = self.convertPun(weibo_content)
        weibo_content = self.removeTopic(weibo_content)
        weibo_content = self.removeBracket(weibo_content)
        weibo_content = self.removePrivate(weibo_content)
        weibo_content = self.removeForward(weibo_content)
        weibo_content = weibo_content.replace(' ', '')

        return weibo_content

    def read_and_filter_api_microblog_data_polarity(self, input_path, polarity):
        polarity_results = []
        with open(input_path) as microblogs_file:
            pos_results, neg_results = [], []
            weibo_id = 1
            for text in microblogs_file:
                cur_list = []
                text = text.rstrip()
                text = self.text_filters(text)
                cur_list.append(str(weibo_id))
                cur_list.append(text)
                cur_list.append(polarity)
                polarity_results.append(cur_list)
                weibo_id = weibo_id + 1
        return polarity_results

    def read_and_filter_api_microblog_data(self, microblog_type):

        if microblog_type == 'training':
            input_positive_path = CURRENT_DIR_PATH + POSITIVE_WEIBO_TRAINING_PATH
            input_negative_path = CURRENT_DIR_PATH + NEGATIVE_WEIBO_TRAINING_PATH
            input_neutral_path = CURRENT_DIR_PATH + NEUTRAL_WEIBO_TRAINING_PATH
        else:
            input_positive_path = CURRENT_DIR_PATH + POSITIVE_WEIBO_TEST_PATH
            input_negative_path = CURRENT_DIR_PATH + NEGATIVE_WEIBO_TEST_PATH
            input_neutral_path = CURRENT_DIR_PATH + NEUTRAL_WEIBO_TEST_PATH
        pos_results = self.read_and_filter_api_microblog_data_polarity(input_positive_path, 'pos')
        neg_results = self.read_and_filter_api_microblog_data_polarity(input_negative_path, 'neg')
        neu_results = self.read_and_filter_api_microblog_data_polarity(input_neutral_path, 'neu')
        weibo_dict = {}
        weibo_dict['pos'] = pos_results
        weibo_dict['neg'] = neg_results
        weibo_dict['neu'] = neu_results
        return weibo_dict








