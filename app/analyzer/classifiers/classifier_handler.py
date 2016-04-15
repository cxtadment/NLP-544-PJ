import os
import nltk
from nltk.corpus import movie_reviews
import pickle
from app.analyzer.classifiers.classifiers import origin_nb_classifier, multinomial_nb_classifer, bernoulli_nb_classifer, \
    logistic_regression_classifier, perceptron_classifier, origin_svc_classifier, linearSVC_classifier, nuSVC_classifier
from app.models import TestResult

CURRENT_DIR_PATH = os.path.dirname(os.path.dirname(__file__)) + '/modules/'

ORIGIN_NB_PATH = CURRENT_DIR_PATH + 'originNB.pickle'
MULTINOMIAL_NB_PATH = CURRENT_DIR_PATH + 'multinomialNB.pickle'
BERNOULLI_NB_PATH = CURRENT_DIR_PATH + 'bernoulliNB.pickle'
LOGISTIC_REGRESSION_PATH = CURRENT_DIR_PATH + 'logisticRegression.pickle'
PERCEPTRON_PATH = CURRENT_DIR_PATH + 'perceptron.pickle'
ORIGIN_SVC_PATH = CURRENT_DIR_PATH + 'svc.pickle'
LINEAR_SVC_PATH = CURRENT_DIR_PATH + 'linearSVC.pickle'
NU_SVC_PATH = CURRENT_DIR_PATH + 'nuSVC.pickle'

classifier_path_list = [('origin_nb', ORIGIN_NB_PATH), ('multinomial_nb', MULTINOMIAL_NB_PATH), ('bernoulli_nb', BERNOULLI_NB_PATH),
                        ('logistic_regression', LOGISTIC_REGRESSION_PATH), ('perceptron', PERCEPTRON_PATH), ('svc', ORIGIN_SVC_PATH),
                        ('linear_svc', LINEAR_SVC_PATH), ('nu_svc', NU_SVC_PATH)]


def test_data():
    documents  = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]

    all_words = []

    for w in movie_reviews.words():
        all_words.append(w.lower())

    all_words = nltk.FreqDist(all_words)

    word_features = list(all_words.keys())[:3000]

    def find_features(document):
        words = set(document)
        features = {}
        for w in word_features:
            features[w] = (w in words)

        return features

    feature_sets = [(find_features(rev), category) for (rev, category) in documents]

    train_set = feature_sets[:1900]
    test_set = feature_sets[1900:]

    return train_set, test_set


def module_build():

    train_set, test_set = test_data()

    #naive bayes classifiers
    origin_nb_classifier(train_set, ORIGIN_NB_PATH)
    multinomial_nb_classifer(train_set, MULTINOMIAL_NB_PATH)
    bernoulli_nb_classifer(train_set, BERNOULLI_NB_PATH)

    #linear classifiers
    logistic_regression_classifier(train_set, LOGISTIC_REGRESSION_PATH)
    perceptron_classifier(train_set, PERCEPTRON_PATH)

    #svm classifiers
    origin_svc_classifier(train_set, ORIGIN_SVC_PATH)
    linearSVC_classifier(train_set, LINEAR_SVC_PATH)
    nuSVC_classifier(train_set, NU_SVC_PATH)




def classify():
    train_set, test_set = test_data()
    for (name, input_path) in classifier_path_list:
        with open(input_path, 'rb') as input_classifier:
            classifier = pickle.load(input_classifier)
            precision = (nltk.classify.accuracy(classifier, test_set)) * 100
            print(name + ' precision is: ', precision)
            testResult = TestResult(classifier=name, probability=precision)
            testResult.save()
            # classifier.show_most_informative_features(15)
