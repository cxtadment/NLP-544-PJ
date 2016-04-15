import nltk
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.svm import SVC, LinearSVC, NuSVC


def write_module(classifer, output_path):
    with open(output_path, 'wb') as output_file:
        pickle.dump(classifer, output_file)


def origin_nb_classifier(train_set, output_path):
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    write_module(classifier, output_path)


def multinomial_nb_classifer(train_set, output_path):
    classifier = SklearnClassifier(MultinomialNB()).train(train_set)
    write_module(classifier, output_path)


def bernoulli_nb_classifer(train_set, output_path):
    classifier = SklearnClassifier(BernoulliNB()).train(train_set)
    write_module(classifier, output_path)


def logistic_regression_classifier(train_set, out_path):
    classifier = SklearnClassifier(LogisticRegression()).train(train_set)
    write_module(classifier, out_path)


def perceptron_classifier(train_set, output_path):
    classifier = SklearnClassifier(Perceptron()).train(train_set)
    write_module(classifier, output_path)


def origin_svc_classifier(train_set, output_path):
    classifier = SklearnClassifier(SVC()).train(train_set)
    write_module(classifier, output_path)


def linearSVC_classifier(train_set, output_path):
    classifier = SklearnClassifier(LinearSVC()).train(train_set)
    write_module(classifier, output_path)


def nuSVC_classifier(train_set, output_path):
    classifier = SklearnClassifier(NuSVC()).train(train_set)
    write_module(classifier, output_path)

