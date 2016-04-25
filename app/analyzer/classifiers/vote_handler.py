from statistics import mode
from nltk.classify import ClassifierI


class VoteClassifier(ClassifierI):

    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        polarity = max(set(votes), key=votes.count)
        return polarity

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        polarity = max(set(votes), key=votes.count)
        chooice_votes = votes.count(polarity)
        conf = chooice_votes / len(votes)
        return conf
