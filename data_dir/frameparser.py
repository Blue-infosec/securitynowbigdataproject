# -*- coding: latin-1 -*-
import random, collections
import csv, nltk, math, nltk.classify, nltk.util, nltk.metrics
from nltk import *
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords

import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures


chezdata = {}
highlyRated = {}
lowRated = {}
trainfeats = {}
testfeats = {}
classifier = {}


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
            '''tweak this number to change the results in the matching precision .0039 is about even distribution
            0.0029 is crazy biased to make most words positive, ends up giving false positives :D oh the irony.
            .0050 gives a smaller positive spectrum but might be more accurate'''
            if chezdata[value][maxval] >= 0.0100:
                highlyRated[value] = chezdata[value][maxval]
            else:
                lowRated[value] = chezdata[value][maxval]


stopset = set(stopwords.words('english'))


def word_feats2(words):
    # print("WORD feats2: {0}".format(words[0]))
    return dict([(words[0], True)])


def word_feats(words):
    return dict([(word, True) for word in words if word not in stopset])


def feature_extractor(doc):
    return doc


def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    # print("BIGRAM WORDS: {0}".format(words[0]))
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    # print("Bigrams Found: {0}".format(dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])))
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])


def bigram_word_feats2(words, score_fn=BigramAssocMeasures.chi_sq, n=100):
    bigram_finder = BigramCollocationFinder.from_words(words[0])
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words[0], bigrams)])


def trigramFeats(thesewords, n=100):
    si = iter(thesewords)
    words = [c + " " + next(si, '') + " " + next(si, '') for c in si]
    tcf = TrigramCollocationFinder.from_words(words)
    tcf.apply_freq_filter(n)
    trigram = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, trigram)])


def Sentiment(sentenceTocheck):
    print classifier.classify(dict([(word, True) for word in sentenceTocheck]))


with open("allSentimentData") as f:
    reader = csv.reader(f, delimiter=" ", quotechar='"')

    map(parseForNltk, reader)
    map(getHighest, chezdata)

    negfeats = list([(word_feats2(f), 'neg') for f in lowRated.iteritems()])
    posfeats = list([(word_feats2(f), 'pos') for f in highlyRated.iteritems()])

    negfeatsB = list([(bigram_word_feats2(f), 'neg') for f in lowRated.iteritems()])
    posfeatsB = list([(bigram_word_feats2(f), 'pos') for f in highlyRated.iteritems()])

    negfeats.extend(negfeatsB)
    posfeats.extend(posfeatsB)

    negidsM = movie_reviews.fileids('neg')
    posidsM = movie_reviews.fileids('pos')

    negfeatsM = [(trigramFeats(movie_reviews.words(fileids=[f])), 'neg') for f in negidsM]
    posfeatsM = [(trigramFeats(movie_reviews.words(fileids=[f])), 'pos') for f in posidsM]

    negfeatsN = [(bigram_word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negidsM]
    posfeatsN = [(bigram_word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posidsM]

    negfeats.extend(negfeatsM)
    posfeats.extend(posfeatsM)

    negfeats.extend(negfeatsN)
    posfeats.extend(posfeatsN)

    random.shuffle(negfeats)
    random.shuffle(posfeats)

    negcutoff = len(negfeats) * 1 / 2
    poscutoff = len(posfeats) * 3 / 4

    print("negfeats type: {0} posfeats type: {1}".format(type(negfeats), type(posfeats)))
    crossover = [item for item in negfeats if item in posfeats]
    print("CROSSOVER chunk should be empty: {0}".format(crossover[5:15]))

    print "negatives: {0} cutoff: {1}".format(len(negfeats), negcutoff)
    print "positives: {0} cutoff: {1}".format(len(posfeats), poscutoff)

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
    print "trainfeats type: {0} length: {1}".format(type(trainfeats), len(trainfeats))

    #training_set = nltk.classify.apply_features(feature_extractor, trainfeats)
    classifier = NaiveBayesClassifier.train(trainfeats)

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

    Sentiment("happy go lucky positive flawless super cheerful awesome translucent moon sun baby father!")
    Sentiment("sad insulting bad day hate filled chocolate poison evil no passed over full metal jacket")
    Sentiment("  What are these guys doing?  Are they trying to put mail servers on my system?  What is their goal?")
    Sentiment("  And ladies and gentlemen, despite all this, he still uses Windows.  I don't know what's wrong with you, Steve.")
    Sentiment("  ...hassle.  And was it you that kind of talked Iomega into admitting that there was a problem?")
    Sentiment("  So we've talked a little bit about, just to recap, the fact that a router makes a very good inbound firewall.  If you want further protection, a software firewall will protect you against outbound traffic.  There is an exception, though.  Routers, in order to do some things on the Internet, you have to poke a hole in the router.")
    Sentiment("  Oh, interesting.  Because it may, in fact, retain some of those port-forwarding settings.  Now, frequently people will do port-forwarding intentionally.  If I want to use BitTorrent or MSN Messenger, I will, in order to use it, I will have to do some port-forwarding.  I will have to open up some holes in my router.  But at least I'm doing that explicitly.")
    Sentiment("This work is licensed for the good of the Internet Community under the ")
    Sentiment("  Oh, and another nice feature of Security Now!, Steve Gibson has decided to foot the bill for transcripts.  So does that mean we'll have full text of each podcast, Steve?")
    Sentiment("  But on the other hand, if it is on your machine, it could turn off the software firewall; whereas, if the bad guy's on somebody else's machine on my network, at least my firewall will protect me.")
    Sentiment("  It just may catch some compromises.")
    Sentiment('"  This is Security Now! with Steve Gibson, Episode 4 for September 8, 2005:  Passwords.  Steve Gibson is on the line, our security wizard, the king of security, the guy who coined the term ""spyware,"" of course created ShieldsUP!, which has saved almost 40 million people from themselves."')

