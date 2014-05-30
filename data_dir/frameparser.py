# -*- coding: latin-1 -*-
import random
import csv,nltk,math
from pymongo import MongoClient
from nltk import *
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords

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
    if value not in stopwords.words('english'):
        if value is not "":
            maxval = max(chezdata[value], key=chezdata[value].get)
            if chezdata[value][maxval] >= 0.0025:
                highlyRated[value] = chezdata[value][maxval]
            else:
                lowRated[value] = chezdata[value][maxval]

def word_feats2(words):
    return dict([(words[0], True)])

def word_feats(words):
    return dict([(w, True) for w in words])

def feature_extractor(doc):
    return doc

def Sentiment(sentenceTocheck):
    print classifier.classify(dict([(word, True) for word in sentenceTocheck]))

with open("allSentimentData") as f:
    reader = csv.reader(f, delimiter=" ")
    map(parseForNltk, reader)
    map(getHighest, chezdata)

    negfeats = list([(word_feats2(f), 'neg') for f in lowRated.iteritems()])
    posfeats = list([(word_feats2(f), 'pos') for f in highlyRated.iteritems()])

    negidsM = movie_reviews.fileids('neg')
    posidsM = movie_reviews.fileids('pos')

    negfeatsM = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negidsM]
    posfeatsM = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posidsM]

    negfeats.extend(negfeatsM)
    posfeats.extend(posfeatsM)

    random.shuffle(negfeats)
    random.shuffle(posfeats)

    negcutoff = len(negfeats) * 1 / 10
    poscutoff = len(posfeats) * 1 / 10

    print "negatives: {0} cutoff: {1}".format(len(negfeats), negcutoff)
    print "positives: {0} cutoff: {1}".format(len(posfeats), poscutoff)

    trainfeats = negfeats[:7000] + posfeats[:7000]
    testfeats = negfeats[1000:3000] + posfeats[4000:7000]

    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
    training_set = nltk.classify.apply_features(feature_extractor, trainfeats)
    #print("TRAINING SET {0}".format(training_set))

    classifier = NaiveBayesClassifier.train(training_set)
    #classifier = PositiveNaiveBayesClassifier.train(map(feature_extractor, trainfeats), map(feature_extractor,testfeats))

    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    print "classifier labels: {0}".format(classifier.labels())
    print "more informatin: {0}".format(classifier.most_informative_features())

    Sentiment("happy go lucky positive cheery super cheerful awesome translucent moon sun baby father")


