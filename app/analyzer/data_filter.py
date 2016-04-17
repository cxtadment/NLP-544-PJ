#!/usr/bin/python
# coding:utf-8
import re
import codecs
import sys
import os

# start of tokenization
# convert chinese punctuation to engnish version

TRAINING_INPUT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/data/SIGHAN8-Task2-Corpus-Release/'
TESTING_INPUT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/data/SIGHAN8-Task2-Corpus/'
CURRENT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/polarity/'
POSITIVE_WEIBO_PATH = "positive_weibo.txt"
NEGATIVE_WEIBO_PATH = "negative_weibo.txt"

def convertPun(content):
    punctuation_list = ['，', '。', '？', '！', '……', ':', '「', '」', '.....', '】', '：', '、']
    punctuation_list2 = ['《', '》', '“', '”', '"', '"']
    for i in range(0, len(punctuation_list)):
        content = content.replace(punctuation_list[i], '.')
        content = content.replace('【', ' ')
    for i in range(0, len(punctuation_list2)):
        content = content.replace(punctuation_list2[i], '')
    return content


# remove http link
def removeLink(content):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    for i in range(0, len(urls)):
        content = content.replace(urls[i], '')
    return content


# remove topic including chinese
def removeTopic(content):
    topics = re.findall(u"#[\w\u0000-\u9FFF]+#", content)
    for i in range(0, len(topics)):
        content = content.replace(topics[i], '')
    return content


# remove content in (), like
def removeBracket(content):
    content = content.replace('（', '(')
    content = content.replace('）', ')')
    brackets = re.findall(u"\([\w\u0000-\u9FFF]+\)", content)
    for i in range(0, len(brackets)):
        content = content.replace(brackets[i], '')
    return content


# remove private messages
def removePrivate(content):
    # privates=re.findall(u"@[\w\u0000-\u9FFF]+",content.decode('utf8'))
    privates = re.findall(u"@[\w\u0000-\u9FFF]+", content)
    for i in range(0, len(privates)):
        content = content.replace(privates[i], '')
    return content


# remove forwarded messages
def removeForward(content):
    forward_index = content.find("//")
    if not forward_index == -1:
        content = content[0:forward_index]
    return content


def read_annotation_data(input_path):

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


def text_filters(weibo_content):

    weibo_content = weibo_content.replace(' ', '')
    weibo_content = removeLink(weibo_content)
    weibo_content = convertPun(weibo_content)
    weibo_content = removeTopic(weibo_content)
    weibo_content = removeBracket(weibo_content)
    weibo_content = removePrivate(weibo_content)
    weibo_content = removeForward(weibo_content)
    weibo_content = weibo_content.replace(' ', '')

    return weibo_content


def read_and_filter_microblog_data(input_path, pos_list, neg_list):

    with open(input_path, 'r') as microblogs_file:
        pos_results, neg_results, neu_results = [], [], []
        for line in microblogs_file:
            # remove '\n' at the end of line
            line = line.rstrip()
            start_left_index = line.find('<')
            start_right_index = line.find('>')
            if start_left_index == -1 or start_right_index == -1:
                continue
            weibo_id = line[start_left_index + 1:start_right_index]
            end_index = line.find(weibo_id, start_right_index + 1)
            weibo_content = line[start_right_index + 2:end_index - 2]

            # tokenization start-------------------------------
            weibo_content = text_filters(weibo_content)
            # tokenization end----------------------------------

            weibo_content.rstrip()
            weibo_polarity = 0
            cur_list = []
            cur_list.append(weibo_id)
            cur_list.append(weibo_content)
            if weibo_id in pos_list:
                cur_list.append("pos")
                pos_results.append(cur_list)
            elif weibo_id in neg_list:
                cur_list.append("neg")
                neg_results.append(cur_list)

        weibo_dict = {}
        weibo_dict['positive'], weibo_dict['negative'] = pos_results, neg_results

        return weibo_dict



# end of tokenization
def read_and_filter_data(microblog_type):
    input_path_root = TRAINING_INPUT_PATH if microblog_type == 'training' else TESTING_INPUT_PATH

    # read annotation file to get weibo id
    input_annotation_path = input_path_root + 'Annotation.txt'
    pos_list, neg_list = read_annotation_data(input_annotation_path)

    # read message file to get weibo content
    input_microblog_path = input_path_root + 'Message.txt'
    weibo_dict = read_and_filter_microblog_data(input_microblog_path, pos_list, neg_list)

    return weibo_dict

def read_and_filter_api_microblog_data(polarity):
	input_path = ""
	if polarity == 'positive':
		input_path = POSITIVE_WEIBO_PATH
	else:
		input_path = NEGATIVE_WEIBO_PATH
	with open(input_path) as microblogs_file:
		pos_results, neg_results = [], []
		weibo_id = 1
		for text in microblogs_file:
			cur_list = []
			text = text.rstrip()
			# tokenization start-------------------------------
            text = text.replace(' ', '')
            text = removeLink(text)
            text = convertPun(text)
            text = removeTopic(text)
            text = removeBracket(text)
            text = removePrivate(text)
           	text = removeForward(text)
            text = text.replace(' ', '')
            # tokenization end----------------------------------
            cur_list.append(weibo_id)
            cur_list.append(text)
            if polarity == 'positive':
            	pos_results.append(cur_list)
            else:
            	neg_results.append(cur_list)
            weibo_id = weibo_id + 1
        weibo_dict = {}
        weibo_dict['positive'] = pos_results
        weibo_dict['negative'] = neg_results
    return weibo_dict        







