#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pickle
import xml.etree.ElementTree as etree

def _parseFile(file, taggedCorpus):
    tree = etree.parse(file)
    root = tree.getroot()
    sentences = root.findall("SENT")
    for sentence in sentences:
        words = sentence.findall("w")

        taggedSentence = []
        for word in words:
            try:
                if word.text is None:
                    continue
                elif len(word) > 0:
                    taggedSentence.append((word.attrib['lemma'].lower(), word.attrib['cat']))
                elif word.text is not None:
                    taggedSentence.append((word.text.lower(), word.attrib['cat']))
            except:
                print(file + " - " + etree.tostring(word))
                pass

        if len(taggedSentence) > 0:
            taggedCorpus.append(taggedSentence)


def createTaggedCorpus(corpusName, inputDirectory, outputDirectory):
    files = os.listdir(inputDirectory)

    taggedCorpus = []
    for file in files:
        _parseFile(inputDirectory + '/' + file, taggedCorpus)

    pickle.dump(taggedCorpus, open(outputDirectory + '/' + corpusName + 'Sentences.pickle', 'wb'))


if __name__ == "__main__":
    createTaggedCorpus('train', '../../resources/FrenchTreebank/corpus-tagged-train', '../../resources/corpus')
    createTaggedCorpus('test', '../../resources/FrenchTreebank/corpus-tagged-test', '../../resources/corpus')
