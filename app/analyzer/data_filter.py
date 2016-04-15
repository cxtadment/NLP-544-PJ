#!/usr/bin/python
# coding:utf-8
import re
import codecs
import sys

# start of tokenization
# convert chinese punctuation to engnish version


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


# remove content in (), like (分享自 @Flyme阅读)
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


# end of tokenization
def readWeibo():
    # read annotation file to get weibo id
    annotation_file = open(
        '/Users/sx/Desktop/CSCI544/FinalProject/Weibo/Dataset/fuzhou/SIGHAN8-Task2-Corpus/Annotation.txt', 'r')
    pos_list = []
    neg_list = []
    neu_list = []
    for line in annotation_file:
        # remove '\n' at the end of line
        line = line.rstrip()
        line_list = line.split('	')
        wid = line_list[3]
        num = line_list[4]
        if num == '1':
            pos_list.append(wid)
        elif num == '-1':
            neg_list.append(wid)
        elif num == '0':
            neu_list.append(wid)
    annotation_file.close()
    # read message file to get weibo content

    pos_results = []
    neg_results = []
    neu_results = []
    weibo_dict = {}
    message_file = codecs.open(
        '/Users/sx/Desktop/CSCI544/FinalProject/Weibo/Dataset/fuzhou/SIGHAN8-Task2-Corpus/Message.txt', 'r', 'utf-8')
    count = 0
    for line in message_file:
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
        weibo_content = weibo_content.replace(' ', '')
        weibo_content = removeLink(weibo_content)
        weibo_content = convertPun(weibo_content)
        weibo_content = removeTopic(weibo_content)
        weibo_content = removeBracket(weibo_content)
        weibo_content = removePrivate(weibo_content)
        weibo_content = removeForward(weibo_content)
        weibo_content = weibo_content.replace(' ', '')
        # tokenization end----------------------------------
        weibo_content.rstrip()
        weibo_polarity = 0
        cur_list = []
        cur_list.append(weibo_id)
        cur_list.append(weibo_content)
        if weibo_id in pos_list:
            cur_list.append("1")
            pos_results.append(cur_list)
        elif weibo_id in neg_list:
            cur_list.append("-1")
            neg_results.append(cur_list)
        else:
            cur_list.append("0")
            neu_results.append(cur_list)
    weibo_dict['positive'] = pos_results
    weibo_dict['negative'] = neg_results
    weibo_dict['neutral'] = neu_results
    return weibo_dict


