
import os
import nltk
from nltk.metrics import precision, recall, f_measure
import pickle
from app.analyzer.classifiers.classifiers import origin_nb_classifier, multinomial_nb_classifer, \
    logistic_regression_classifier, linearSVC_classifier, random_forest_classifier
from app.analyzer.classifiers.vote_handler import VoteClassifier
from app.models import TestResult, Microblog, SearchResult
from collections import defaultdict
import random



CURRENT_DIR_PATH = os.path.dirname(os.path.dirname(__file__)) + '/pickles/'

WORDS_FEATURES_PATH = CURRENT_DIR_PATH + 'wordsFeature.pickle'
FEATURE_SET_PATH = CURRENT_DIR_PATH + 'featureSet.pickle'

ORIGIN_NB_PATH = CURRENT_DIR_PATH + 'originNB.pickle'
MULTINOMIAL_NB_PATH = CURRENT_DIR_PATH + 'multinomialNB.pickle'
BERNOULLI_NB_PATH = CURRENT_DIR_PATH + 'bernoulliNB.pickle'
LOGISTIC_REGRESSION_PATH = CURRENT_DIR_PATH + 'logisticRegression.pickle'
PERCEPTRON_PATH = CURRENT_DIR_PATH + 'perceptron.pickle'
LINEAR_SVC_PATH = CURRENT_DIR_PATH + 'linearSVC.pickle'
RANDOM_FOREST_PATH = CURRENT_DIR_PATH + 'random_forest.pickle'

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

    words_features = list(all_words.keys())[:1400]

    with open(WORDS_FEATURES_PATH, 'wb') as output_file:
        pickle.dump(words_features, output_file)


def feature_filter(document, words_features):
    words = set(document)
    features = {}
    for w in words_features:
        features[w] = (w in words)

    return features


# def get_feature_set_for_api(words, words_features):

def pickle_feature_set(feature_set):
    with open(FEATURE_SET_PATH, 'wb') as output_file:
        pickle.dump(feature_set, output_file)

def get_pickle_feature_set():
    with open(FEATURE_SET_PATH, 'rb') as input_file:
        feature_set = pickle.load(input_file)
        return feature_set


def get_feature_set(microblogType):

    microblogs = Microblog.objects()

    words_features = get_words_features_pickle()

    feature_sets = [(feature_filter(microblog.words,  words_features), microblog.polarity) for microblog in microblogs]

    random.shuffle(feature_sets)

    pickle_feature_set(feature_sets)


    return feature_sets


def module_build():

    pickle_words_features('training')
    train_set = get_feature_set('training')
    train_set = train_set[2000:]

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


def overall_score_calculator(pos, neg, pos_count, neg_count):
    return round(float((pos*pos_count + neg*neg_count) / (pos_count + neg_count)), 2)


def sub_score_calculator(label, refsets, testsets):
    res_precision = precision(refsets[label], testsets[label])
    res_recall = recall(refsets[label], testsets[label])
    res_f_score = f_measure(refsets[label], testsets[label])

    return round(res_precision, 2), round(res_recall, 2), round(res_f_score, 2)


def save_testing_result(classifier, test_feats, classifier_name):

    refsets = defaultdict(set)
    testsets = defaultdict(set)

    for i, (feats, label) in enumerate(test_feats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    pos_count, neg_count  = len(refsets['pos']), len(refsets['neg'])
    pos_precision, pos_recall, pos_f_score = sub_score_calculator('pos', refsets, testsets)
    neg_precision, neg_recall, neg_f_score = sub_score_calculator('neg', refsets, testsets)

    overall_precision = overall_score_calculator(pos_precision, neg_precision, pos_count, neg_count)
    overall_recall = overall_score_calculator(pos_recall, neg_recall, pos_count, neg_count)
    overall_f_score = round(2*(overall_precision*overall_recall) / (overall_precision + overall_recall), 2)

    # accuracy = (nltk.classify.accuracy(classifier, test_feats)) * 100

    testResult = TestResult(classifier=classifier_name,  pos_count=pos_count, neg_count=neg_count,
                            pos_precision=pos_precision, pos_recall=pos_recall, pos_f_score=pos_f_score,
                            neg_precision=neg_precision, neg_recall=neg_recall, neg_f_score=neg_f_score,
                            precision=overall_precision, recall=overall_recall, f_score=overall_f_score)
    testResult.save()


def baseline_method():
    microblogs = Microblog.objects(microblogType='training')
    refsets = defaultdict(set)
    testsets = defaultdict(set)

    for i, microblog in enumerate(microblogs):
        refsets[microblog.polarity].add(i)
        if microblog.negCount < microblog.posCount:
            testsets['pos'].add(i)
        else:
            testsets['neg'].add(i)
    pos_count, neg_count = len(refsets['pos']), len(refsets['neg'])
    pos_precision, pos_recall, pos_f_score = sub_score_calculator('pos', refsets, testsets)
    neg_precision, neg_recall, neg_f_score = sub_score_calculator('neg', refsets, testsets)

    overall_precision = overall_score_calculator(pos_precision, neg_precision, pos_count, neg_count)
    overall_recall = overall_score_calculator(pos_recall, neg_recall, pos_count, neg_count)
    overall_f_score = round(2*(overall_precision*overall_recall) / (overall_precision + overall_recall), 2)

    # print(overall_precision)
    # accuracy = (nltk.classify.accuracy(classifier, test_feats)) * 100

    testResult = TestResult(classifier='Baseline',  pos_count=pos_count, neg_count=neg_count,
                            pos_precision=pos_precision, pos_recall=pos_recall, pos_f_score=pos_f_score,
                            neg_precision=neg_precision, neg_recall=neg_recall, neg_f_score=neg_f_score,
                            precision=overall_precision, recall=overall_recall, f_score=overall_f_score)
    testResult.save()


def classify_testing():


    test_set = get_pickle_feature_set()
    random.shuffle(test_set)
    test_set = test_set[:2000]

    baseline_method()

    for (name, input_path) in classifier_path_list:
        with open(input_path, 'rb') as input_classifier:
            classifier = pickle.load(input_classifier)
            save_testing_result(classifier, test_set, name)
            # classifier.show_most_informative_features(25)


def get_classifier(classifier_path):
    with open(classifier_path, 'rb') as input_classifier:
        classifier = pickle.load(input_classifier)
        return classifier


class ApiClassifier:

    def __init__(self):
        self.nb_classifier, self.mu_nb_classifier, self.lg_re_classifier = get_classifier(ORIGIN_NB_PATH), get_classifier(MULTINOMIAL_NB_PATH), get_classifier(LOGISTIC_REGRESSION_PATH)
        self.li_svc_classifier, self.random_forest_classifier = get_classifier(LINEAR_SVC_PATH), get_classifier(RANDOM_FOREST_PATH)
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

# def classify_data_from_api(data):
#     test_set = None
#     for microblog in data:
#         for (name, input_path) in classifier_path_list:
#             with open(input_path, 'rb') as input_classifier: