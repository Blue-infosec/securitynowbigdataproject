import sys, re
import nltk
import pymongo
import csv
from pymongo import MongoClient
from operator import add
from pyspark import SparkContext
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.tokenize import *
from nltk import *


def word_feats(words):
    return dict([(word, True) for word in words])


negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

negcutoff = len(negfeats) * 3 / 4
poscutoff = len(posfeats) * 3 / 4

trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

classifier = NaiveBayesClassifier.train(trainfeats)
print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
classifier.show_most_informative_features()

mongo = MongoClient('172.17.0.5', 27017)
mdb = mongo['twapp_storage']
secnow = mongo.securitynow
secnow_c = secnow.securitynow


def mapper(line, title, secfile, idsec):
    post = mdb.posts
    tokens = word_tokenize(line)
    tagged = pos_tag(tokens)
    ntities = chunk.ne_chunk(tagged)

    newline = line.encode('utf-8')

    sentclas = dict([(word, True) for word in newline])

    print "nltk entities:"
    for tag in ntities:
        print "Entity: {0} </entity>".format(tag) if "NNP" in tag else ""

    posting = {"securitynow_id": idsec, "episode": secfile[3:6], "speaker": title, "original": line, "tokens": tokens,
               "entities": ntities, "sentiment": classifier.classify(sentclas)}
    post_id = post.insert(posting)

    print "saved to mongo, post id: {0}".format(post_id)


if __name__ == "__main__":
    sc = SparkContext(sys.argv[1], "sentiment")
    lines = sc.textFile(sys.argv[2])

    for post in secnow_c.find({"Titles": {"$regex": u"LEO"}}):
        print post
        mapper(post['Data'], post['Titles'], post['File'], post['_id'])

    for post in secnow_c.find({"Titles": {"$regex": u"STEVE"}}):
        print post
        mapper(post['Data'])

    print "mapper completed"