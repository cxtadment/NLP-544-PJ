
import os
import nltk
import operator
import re
from nltk.metrics import precision, recall, f_measure
import pickle
from app.analyzer.classifiers.classifiers import origin_nb_classifier, multinomial_nb_classifer, \
    logistic_regression_classifier, linearSVC_classifier, random_forest_classifier
from app.analyzer.classifiers.vote_handler import VoteClassifier
from app.models import TestResult, Microblog, SearchResult
from collections import defaultdict




CURRENT_DIR_PATH = os.path.dirname(os.path.dirname(__file__)) + '/pickles/'
RESOURCES_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/resources/'
WORDS_FEATURES_PATH = CURRENT_DIR_PATH + 'wordsFeature.pickle'
FEATURE_SET_PATH = CURRENT_DIR_PATH + 'featureSet.pickle'

ORIGIN_NB_PATH = CURRENT_DIR_PATH + 'originNB.pickle'
MULTINOMIAL_NB_PATH = CURRENT_DIR_PATH + 'multinomialNB.pickle'
BERNOULLI_NB_PATH = CURRENT_DIR_PATH + 'bernoulliNB.pickle'
LOGISTIC_REGRESSION_PATH = CURRENT_DIR_PATH + 'logisticRegression.pickle'
PERCEPTRON_PATH = CURRENT_DIR_PATH + 'perceptron.pickle'
LINEAR_SVC_PATH = CURRENT_DIR_PATH + 'linearSVC.pickle'
RANDOM_FOREST_PATH = CURRENT_DIR_PATH + 'random_forest.pickle'
NEGATIVE_WORDS_PATH = RESOURCES_PATH + 'sentiment_zh/combineNegative.txt'
POSITIVE_WORDS_PATH = RESOURCES_PATH + 'sentiment_zh/combinePositive.txt'
POSITIVE_EMOTICONS_PATH = RESOURCES_PATH + 'emotion/positive_emoticons.txt'
NEGATIVE_EMOTICONS_PATH = RESOURCES_PATH + 'emotion/negative_emoticons.txt'

classifier_path_list = [('Naive Bayes', ORIGIN_NB_PATH), ('Multinomial Naive Bayes', MULTINOMIAL_NB_PATH),
                        ('Logistic Regression', LOGISTIC_REGRESSION_PATH), ('Linear SVC', LINEAR_SVC_PATH),
                        ('Random Forest', RANDOM_FOREST_PATH)]

TAGGING_CHOOSE = set(['nr', 'n', 'ul'])


def get_words_features_pickle():
    with open(WORDS_FEATURES_PATH, 'rb') as input_file:
        return pickle.load(input_file)


def pickle_words_features(microblogType):
    microblogs = Microblog.objects(microblogType=microblogType)

    all_words = []
    for microblog in microblogs:
        all_words.extend(microblog.words)
    all_words = nltk.FreqDist(all_words)

    words_features = list(all_words.keys())[:3000]

    with open(WORDS_FEATURES_PATH, 'wb') as output_file:
        pickle.dump(words_features, output_file)


def feature_filter(document, words_features):
    words = set(document)
    features = {}
    for w in words_features:
        features[w] = (w in words)

    return features


def get_feature_set(microblogType):

    microblogs = Microblog.objects()

    words_features = get_words_features_pickle()

    feature_sets = [(feature_filter(microblog.words,  words_features), microblog.polarity) for microblog in microblogs]


    return feature_sets


def module_build():
    pickle_words_features('training')
    train_set = get_feature_set('training')

    #naive bayes classifiers
    origin_nb_classifier(train_set, ORIGIN_NB_PATH)
    multinomial_nb_classifer(train_set, MULTINOMIAL_NB_PATH)
    # bernoulli_nb_classifer(train_set, BERNOULLI_NB_PATH)

    #linear classifiers
    logistic_regression_classifier(train_set, LOGISTIC_REGRESSION_PATH)
    # perceptron_classifier(train_set, PERCEPTRON_PATH)

    #svm classifiers
    linearSVC_classifier(train_set, LINEAR_SVC_PATH)

    #random forest
    random_forest_classifier(train_set, RANDOM_FOREST_PATH)


def overall_score_calculator(pos, neg, neu, pos_count, neg_count, neu_count):
    return round(float((pos*pos_count + neg*neg_count + neu*neu_count) / (pos_count + neg_count + neu_count)), 2)


def sub_score_calculator(label, refsets, testsets):
    res_precision = precision(refsets[label], testsets[label])
    res_recall = recall(refsets[label], testsets[label])
    res_f_score = f_measure(refsets[label], testsets[label])

    return round(res_precision, 2), round(res_recall, 2), round(res_f_score, 2)


def save_to_database(refsets, testsets, classifier_name):

    pos_count, neg_count, neu_count = len(refsets['pos']), len(refsets['neg']), len(refsets['neu'])
    pos_precision, pos_recall, pos_f_score = sub_score_calculator('pos', refsets, testsets)
    neg_precision, neg_recall, neg_f_score = sub_score_calculator('neg', refsets, testsets)
    neu_precision, neu_recall, neu_f_score = sub_score_calculator('neu', refsets, testsets)

    overall_precision = overall_score_calculator(pos_precision, neg_precision, neu_precision, pos_count, neg_count, neu_count)
    overall_recall = overall_score_calculator(pos_recall, neg_recall, neu_recall, pos_count, neg_count, neu_count)
    overall_f_score = round(2*(overall_precision*overall_recall) / (overall_precision + overall_recall), 2)

    testResult = TestResult(classifier=classifier_name,  pos_count=pos_count, neg_count=neg_count,
                            pos_precision=pos_precision, pos_recall=pos_recall, pos_f_score=pos_f_score,
                            neg_precision=neg_precision, neg_recall=neg_recall, neg_f_score=neg_f_score,
                            neu_precision=neu_precision, neu_recall=neu_recall, neu_f_score=neu_f_score,
                            precision=overall_precision, recall=overall_recall, f_score=overall_f_score)
    testResult.save()


def save_testing_result(classifier, test_feats, classifier_name):

    refsets = defaultdict(set)
    testsets = defaultdict(set)

    for i, (feats, label) in enumerate(test_feats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    save_to_database(refsets, testsets, classifier_name)


def baseline_method():
    microblogs = Microblog.objects(microblogType='training')
    refsets = defaultdict(set)
    testsets = defaultdict(set)

    for i, microblog in enumerate(microblogs):
        refsets[microblog.polarity].add(i)
        if microblog.negCount < microblog.posCount:
            testsets['pos'].add(i)
        elif microblog.negCount > microblog.posCount:
            testsets['neg'].add(i)
        else:
            testsets['neu'].add(i)

    save_to_database(refsets, testsets, 'Baseline')


def classify_testing():

    test_set = get_feature_set('testing')

    baseline_method()


    for (name, input_path) in classifier_path_list:
        with open(input_path, 'rb') as input_classifier:
            classifier = pickle.load(input_classifier)
            save_testing_result(classifier, test_set, name)


def get_classifier(classifier_path):
    with open(classifier_path, 'rb') as input_classifier:
        classifier = pickle.load(input_classifier)
        return classifier



class ApiClassifier:

    def __init__(self):
        self.nb_classifier, self.mu_nb_classifier, self.lg_re_classifier = get_classifier(ORIGIN_NB_PATH), get_classifier(MULTINOMIAL_NB_PATH), get_classifier(LOGISTIC_REGRESSION_PATH)
        self.li_svc_classifier, self.random_forest_classifier = get_classifier(LINEAR_SVC_PATH), get_classifier(RANDOM_FOREST_PATH)
        with open(NEGATIVE_WORDS_PATH) as negative_words_doc:
            self.negative_words = set([line.rstrip() for line in negative_words_doc])
        with open(POSITIVE_WORDS_PATH) as positive_words_doc:
            self.positive_words = set([line.rstrip() for line in positive_words_doc]) 
        with open(POSITIVE_EMOTICONS_PATH) as positive_emoticons_doc:
            self.positive_emoticons_dict = set([line.rstrip() for line in positive_emoticons_doc])
        with open(NEGATIVE_EMOTICONS_PATH) as negative_emoticons_doc:
            self.negative_emoticons_dict = set([line.rstrip() for line in negative_emoticons_doc]) 

        self.vote_classifier = VoteClassifier(self.nb_classifier, self.mu_nb_classifier, self.lg_re_classifier, self.li_svc_classifier, self.random_forest_classifier)

    def classify(self, microblogs):
        searchResults = []
        words_features = get_words_features_pickle()
        for (text, filter_text, words, taggings) in microblogs:
            test_features = feature_filter(words, words_features)
            polarity = self.vote_classifier.classify(test_features)
            confidence = round(self.vote_classifier.confidence(test_features)*100, 2)
            single_searchResult = SearchResult(text=text, filter_text=filter_text, words=words, polarity=polarity, confidence=confidence)
            searchResults.append(single_searchResult)

        return searchResults

    """

    retrieve pattern

    """

    def pattern_induct(self):
        microblogs = Microblog.objects()
        polarity_pattern_dict = {}
        polarity_pattern_dict['pos'] = {}
        polarity_pattern_dict['neg'] = {}
        for microblog in microblogs:
            polarity = microblog.polarity
            if polarity == 'neu':
                continue
            pattern_dict = polarity_pattern_dict[polarity]
            word_list = microblog.pre_words
            tag_list = microblog.pre_taggings
            for i in range(0, len(tag_list)):
                cur_word = word_list[i]
                if i >= 2:
                    first_tag = tag_list[i - 2]
                    second_tag = tag_list[i - 1]
                    cur_tag = tag_list[i]
                    first_word = word_list[i - 2]
                    second_word = word_list[i - 1]

                    if first_tag == 'ad' and second_tag == 'a' and cur_tag == 'u':
                        if cur_word in pattern_dict:
                            pattern_dict[cur_word] = pattern_dict[cur_word] + 1
                        else:
                            pattern_dict[cur_word] = 1
                if cur_word in self.positive_words and polarity == 'pos' or (
                        cur_word in self.negative_words and polarity == 'neg'):
                    if cur_word in pattern_dict:
                        pattern_dict[cur_word] = pattern_dict[cur_word] + 1
                    else:
                        pattern_dict[cur_word] = 1
            polarity_pattern_dict[polarity] = pattern_dict
        # sort polarity_pattern_dict
        positive_pattern_dict = polarity_pattern_dict['pos']
        negative_pattern_dict = polarity_pattern_dict['neg']
        sorted_positive_pattern_tuple = sorted(positive_pattern_dict.items(), key=operator.itemgetter(1))
        sorted_negative_pattern_tuple = sorted(negative_pattern_dict.items(), key=operator.itemgetter(1))
        sorted_positive_pattern_dict = {}
        sorted_negative_pattern_dict = {}
        for (key, value) in sorted_positive_pattern_tuple[:100]:
            sorted_positive_pattern_dict[key] = value
        for key, value in sorted_negative_pattern_tuple[:100]:
            sorted_negative_pattern_dict[key] = value
        print('sorted_positive_pattern_dict---------------------')
        print(sorted_positive_pattern_dict)
        print('sorted_negative_pattern_dict---------------------')
        print(sorted_negative_pattern_dict)
        return sorted_positive_pattern_dict, sorted_negative_pattern_dict

    """

    retrieve emoticons

    """

    def emoticon_retrieve(self, microblog_list):
        positive_emoticon_count_dict = {}
        negative_emoticon_count_dict = {}
        # add-one smoothing
        for positive_emoticon in self.positive_emoticons_dict:
            positive_emoticon_count_dict[positive_emoticon] = 1
        for negative_emoticon in self.negative.emoticons_dict:
            negative_emoticon_count_dict[negative_emoticon] = 1

        for microblog in microblog_list:
            text_list = microblog[1]
            emoticons = re.findall(u"\[[\w\u0000-\u9FFF]+\]", text_list)
            polarity = microblog[2]
            for emoticon in emoticons:
                if polarity == 'pos' and emoticon in self.positive_emoticons_dict:
                    positive_emoticon_count_dict[emoticon] = positive_emoticon_count_dict[emoticon] + 1
                elif polarity == 'neg' and emoticon in self.negative_emoticons_dict:
                    negative_emoticon_count_dict[emoticon] = negative_emoticon_count_dict[emoticon] + 1

            return positive_emoticon_count_dict, negative_emoticon_count_dict
