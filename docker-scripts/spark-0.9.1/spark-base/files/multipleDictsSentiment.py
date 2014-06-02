# -*- coding: latin-1 -*-
import random, collections
import csv, nltk, math, nltk.classify, nltk.util, nltk.metrics
from pymongo import MongoClient
from nltk import *
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords

import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

chezdata = {}
highlyRated = {}
lowRated = {}
trainfeats = {}
testfeats = {}
classifier = {}

mongo = MongoClient('172.17.0.2', 27017)


def parseForNltk(value):

    try:
        value[2] = int(value[2])
        value[3] = int(value[3])
        value[4] = int(value[4])
    except ValueError as e:
        value[2] = 0
        value[3] = 1
        value[4] = 1

    if value[1] == '':
        value[1] = "empty"

    floater = (float(value[3]) / float(value[4])) * 100

    if chezdata.get(value[1]) is None:
        chezdata[value[1]] = {}

    if value[2] == 1:
        chezdata[value[1]][1] = floater
    if value[2] == 2:
        chezdata[value[1]][2] = floater
    if value[2] == 3:
        chezdata[value[1]][3] = floater
    if value[2] == 4:
        chezdata[value[1]][4] = floater
    if value[2] == 5:
        chezdata[value[1]][5] = floater


def getHighest(value):

    if value is not "":
        maxval = max(chezdata[value], key=chezdata[value].get)

        if chezdata[value][maxval] >= 0.00385:
            highlyRated[value] = chezdata[value][maxval]
        else:
            lowRated[value] = chezdata[value][maxval]

stopset = set(stopwords.words('english'))

def word_feats2(words):
    #print("WORD feats2: {0}".format(words[0]))
    if words[0] not in stopset:
        return dict([(words[0], True)])


def word_feats(words):
    return dict([(word, True) for word in words if word not in stopset])

def feature_extractor(doc):
    return doc

def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    #print("BIGRAM WORDS: {0}".format(words[0]))
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    #print("Bigrams Found: {0}".format(dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])))
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

def Sentiment(sentenceTocheck):
    print classifier.classify(dict([(word, True) for word in sentenceTocheck]))


with open("/data/allSentimentData") as f:
    reader = csv.reader(f, delimiter=" ", quotechar='"')

    map(parseForNltk, reader)
    map(getHighest, chezdata)

    negfeats = list([(word_feats2(f), 'neg') for f in lowRated.iteritems()])
    posfeats = list([(word_feats2(f), 'pos') for f in highlyRated.iteritems()])

    negidsM = movie_reviews.fileids('neg')
    posidsM = movie_reviews.fileids('pos')

    negfeatsM = [(bigram_word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negidsM]
    posfeatsM = [(bigram_word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posidsM]

    negfeats.extend(negfeatsM)
    posfeats.extend(posfeatsM)

    random.shuffle(negfeats)
    random.shuffle(posfeats)

    negcutoff = len(negfeats) * 3/4
    poscutoff = len(posfeats) * 3/4

    print("negfeats type: {0} posfeats type: {1}".format(type(negfeats), type(posfeats)))
    crossover = [item for item in negfeats if item in posfeats]
    print("CROSSOVER chunk should be empty: {0}".format(crossover[5:15]))

    print "negatives: {0} cutoff: {1}".format(len(negfeats), negcutoff)
    print "positives: {0} cutoff: {1}".format(len(posfeats), poscutoff)

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
    # training_set = nltk.classify.apply_features(feature_extractor, trainfeats)
    #print("TRAINING SET {0}".format(training_set))

    #training exactly 7000 each
    classifier = NaiveBayesClassifier.train(trainfeats)
    #classifier = PositiveNaiveBayesClassifier.train(map(feature_extractor, trainfeats), map(feature_extractor,testfeats))

    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    print 'pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos'])
    print 'pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos'])
    print 'neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg'])
    print 'neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg'])
    print "classifier labels: {0}".format(classifier.labels())
    print "more information: {0}".format(classifier.most_informative_features())
    classifier.show_most_informative_features()


