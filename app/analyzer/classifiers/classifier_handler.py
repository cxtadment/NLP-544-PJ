import os
import nltk
from nltk.corpus import movie_reviews
import pickle
from app.analyzer.classifiers.classifiers import origin_nb_classifier, multinomial_nb_classifer, bernoulli_nb_classifer, \
    logistic_regression_classifier, perceptron_classifier, linearSVC_classifier, nuSVC_classifier
from app.analyzer.classifiers.vote_handler import VoteClassifier
from app.models import TestResult, Microblog


CURRENT_DIR_PATH = os.path.dirname(os.path.dirname(__file__)) + '/modules/'

WORDS_FEATURES_PATH = CURRENT_DIR_PATH + '/wordsFeature.pickle'

ORIGIN_NB_PATH = CURRENT_DIR_PATH + 'originNB.pickle'
MULTINOMIAL_NB_PATH = CURRENT_DIR_PATH + 'multinomialNB.pickle'
BERNOULLI_NB_PATH = CURRENT_DIR_PATH + 'bernoulliNB.pickle'
LOGISTIC_REGRESSION_PATH = CURRENT_DIR_PATH + 'logisticRegression.pickle'
PERCEPTRON_PATH = CURRENT_DIR_PATH + 'perceptron.pickle'
LINEAR_SVC_PATH = CURRENT_DIR_PATH + 'linearSVC.pickle'
NU_SVC_PATH = CURRENT_DIR_PATH + 'nuSVC.pickle'

classifier_path_list = [('origin_nb', ORIGIN_NB_PATH), ('multinomial_nb', MULTINOMIAL_NB_PATH), ('bernoulli_nb', BERNOULLI_NB_PATH),
                        ('logistic_regression', LOGISTIC_REGRESSION_PATH), ('perceptron', PERCEPTRON_PATH), ('linear_svc', LINEAR_SVC_PATH),
                        ('nu_svc', NU_SVC_PATH)]

TAGGING_CHOOSE = set(['nr', 'n', 'ul'])


def pickle_words_features():
    microblogs = Microblog.objects(microblogType=0)

    all_words = []
    for microblog in microblogs:
        all_words.extend(microblog.words)
        # for t in range(len(microblog.words)):
        #     if microblog.taggings[t] in TAGGING_CHOOSE:
        #         all_noun_words.extend(microblog.words[t])
        #     elif microblog.taggings[t] == 'a':
        #         all_adj_words.extend(microblog.words[t])

    # all_noun_words = nltk.FreqDist(all_noun_words)
    # all_adj_words = nltk.FreqDist(all_adj_words)
    all_words = nltk.FreqDist(all_words)

    words_features = list(all_words.keys())[:1400]

    with open(WORDS_FEATURES_PATH, 'wb') as output_file:
        pickle.dump(words_features, output_file)

def get_words_features_pickle():
    with open(WORDS_FEATURES_PATH, 'rb') as input_file:
        return pickle.load(input_file)


def feature_filter(document, words_features):
    words = set(document)
    features = {}
    for w in words_features:
        features[w] = (w in words)

    return features


def get_feature_set(microblogType):

    microblogs = Microblog.objects(microblogType=microblogType)

    words_features = get_words_features_pickle()

    feature_sets = [(feature_filter(microblog.words, words_features), microblog.polarity) for microblog in microblogs]

    return feature_sets


def module_build():
    pickle_words_features()
    train_set = get_feature_set(0)
    train_set = train_set[2000:]

    #naive bayes classifiers
    origin_nb_classifier(train_set, ORIGIN_NB_PATH)
    multinomial_nb_classifer(train_set, MULTINOMIAL_NB_PATH)
    bernoulli_nb_classifer(train_set, BERNOULLI_NB_PATH)

    #linear classifiers
    logistic_regression_classifier(train_set, LOGISTIC_REGRESSION_PATH)
    perceptron_classifier(train_set, PERCEPTRON_PATH)

    #svm classifiers
    linearSVC_classifier(train_set, LINEAR_SVC_PATH)
    nuSVC_classifier(train_set, NU_SVC_PATH)


def save_testing_result(classifier, test_set, classifier_name):
    precision = (nltk.classify.accuracy(classifier, test_set)) * 100
    print(classifier_name + ' precision is: ', precision)
    testResult = TestResult(classifier=classifier_name, probability=precision)
    testResult.save()


def classify_testing():
    test_set = get_feature_set(0)
    test_set = test_set[:2000]
    all_classifiers = []
    for (name, input_path) in classifier_path_list:
        with open(input_path, 'rb') as input_classifier:
            classifier = pickle.load(input_classifier)
            all_classifiers.append(classifier)
            save_testing_result(classifier, test_set, name)
            # classifier.show_most_informative_features(15)
    # voted_classifier = VoteClassifier(all_classifiers)
    # save_testing_result(voted_classifier, test_set, 'All in one classifier')


# def classify_data_from_api(data):
#     test_set = None
#     for microblog in data:
#         for (name, input_path) in classifier_path_list:
#             with open(input_path, 'rb') as input_classifier:
