from pyspark import SparkContext
from pyspark import SparkFiles
from pymongo import MongoClient
import random, collections
import csv, nltk, math, nltk.classify, nltk.util, nltk.metrics
from nltk import *
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from IPython.lib import backgroundjobs as bg

import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures

sc = SparkContext()

chezdata = {}
global pchezdata
highlyRated = {}
lowRated = {}
trainfeats = {}
testfeats = {}
global classifier


print("CONNECTING TO MONGO")
mongo = MongoClient('172.17.0.8', 27017)
secnow = mongo.securitynow
secnow_c = secnow.securitynow
mdb = mongo['twapp_sparked_002']
print("CONNECTED TO MONGO")


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

    pchezdata = sc.parallelize(chezdata)

    return chezdata


def getHighest(value):
    #print("GET HIGHEST: {0}".format(value))
    if value not in stopwords.words('english'):
        if value is not "":
            maxval = max(chezdata[value], key=chezdata[value].get)
            '''tweak this number to change the results in the matching precision .0039 is about even distribution
            0.0029 is crazy biased to make most words positive, ends up giving false positives :D oh the irony.
            .0050 gives a smaller positive spectrum but might be more accurate'''
            if chezdata[value][maxval] >= 0.0053:
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


def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=217):
    # print("BIGRAM WORDS: {0}".format(words[0]))
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    # print("Bigrams Found: {0}".format(dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])))
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])


def bigram_word_feats2(words, score_fn=BigramAssocMeasures.chi_sq, n=143):
    bigram_finder = BigramCollocationFinder.from_words(words[0])
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words[0], bigrams)])


def trigramFeats(thesewords, n=57):
    si = iter(thesewords)
    words = [c + " " + next(si, '') + " " + next(si, '') for c in si]
    tcf = TrigramCollocationFinder.from_words(words)
    tcf.apply_freq_filter(n)
    trigram = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, trigram)])


def trainer():

    negfeats = list([(word_feats2(f), 'neg') for f in lowRatedP.collect()])
    posfeats = list([(word_feats2(f), 'pos') for f in highlyRatedP.collect()])

    negfeatsB = list([(bigram_word_feats2(f), 'neg') for f in lowRated.iteritems()])
    posfeatsB = list([(bigram_word_feats2(f), 'pos') for f in highlyRated.iteritems()])

    print("negfeats len DATA: {0}".format(len(negfeats)))
    print("posfeats len DATA: {0}".format(len(posfeats)))

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

    print("after mixins negfeats len DATA: {0}".format(len(negfeats)))
    print("after mixins posfeats len DATA: {0}".format(len(posfeats)))

    random.shuffle(negfeats)
    random.shuffle(posfeats)

    negcutoff = len(negfeats) * 1 / 2
    poscutoff = len(posfeats) * 3 / 4

    crossover = [item for item in negfeats if item in posfeats]
    print("CROSSOVER chunk should be empty: {0}".format(crossover[5:15]))

    print "negatives: {0} cutoff: {1}".format(len(negfeats), negcutoff)
    print "positives: {0} cutoff: {1}".format(len(posfeats), poscutoff)

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
    print "trainfeats type: {0} length: {1}".format(type(trainfeats), len(trainfeats))

    global classifier
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


def mapper(line, title, secfile, idsec):
    post = mdb.posts
    tokens = word_tokenize(line)
    tagged = pos_tag(tokens)
    ntities = chunk.ne_chunk(tagged)
    newline = line.encode('utf-8')

    posting = {"securitynow_id": idsec, "episode": secfile[3:6], "speaker": title, "original": line, "tokens": tokens,
               "entities": ntities, "sentiment": classifier.classify(dict([(word, True) for word in newline]))}
    post_id = post.insert(posting)


sc.addFile("/home/th3m4d0n3/NetBeansProjects/twAppDemo/data_dir/allSentimentData")
with open(SparkFiles.get("allSentimentData")) as f:
    reader = csv.reader(f, delimiter=" ", quotechar='"')

    jobs = bg.BackgroundJobManager()
    map(parseForNltk, reader)

    print("chezdata type DATA: {0} COUNT: {1}".format(type(chezdata), len(chezdata)))

    map(getHighest, chezdata)

    chezdataP = sc.parallelize(chezdata)
    lowRatedP = sc.parallelize(lowRated)
    highlyRatedP = sc.parallelize(highlyRated)

    print("chezdataP type DATA: {0} COUNT: {1}".format(type(chezdataP), chezdataP.count()))
    print("lowRatedP type DATA: {0} COUNT: {1}".format(type(lowRatedP), lowRatedP.count()))
    print("highlyRatedP type DATA: {0} COUNT: {1}".format(type(highlyRatedP), highlyRatedP.count()))

    trainer()

    for post in secnow_c.find({"Titles": {"$regex": u"LEO"}}):
        mapper(post['Data'], post['Titles'], post['File'], post['_id'])

    for post in secnow_c.find({"Titles": {"$regex": u"STEVE"}}):
        mapper(post['Data'], post['Titles'], post['File'], post['_id'])