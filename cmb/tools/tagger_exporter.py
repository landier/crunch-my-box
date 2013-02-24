#!/usr/bin/python
# -*- coding: utf-8 -*-

import cPickle
import nltk

def createAndExportTagger(trainingSetFile):
    # Training set
    trainingSet = cPickle.load(open(trainingSetFile, 'rb'))

    # Taggers
    defaultTagger = nltk.DefaultTagger('N')
    unigramTagger = nltk.UnigramTagger(trainingSet, backoff=defaultTagger)
    bigramTagger = nltk.BigramTagger(trainingSet, backoff=unigramTagger)

    # Serialize tagger
    cPickle.dump(bigramTagger, open('../cruncher/tagger.pickle', 'wb'))


if __name__ == "__main__":
    createAndExportTagger('../../resources/corpus/trainSentences.pickle')
