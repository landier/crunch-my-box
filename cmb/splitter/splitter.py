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
                    taggedSentence.append((word.attrib['lemma'], word.attrib['cat']))
                elif word.text is not None:
                    taggedSentence.append((word.text, word.attrib['cat']))
            except:
                print(file + " - " + etree.tostring(word))
                pass

        taggedCorpus.append(taggedSentence)


def createTaggedCorpus(corpusName, inputDirectory):
    files = os.listdir(inputDirectory)

    taggedCorpus = []
    for file in files:
        _parseFile(inputDirectory + '/' + file, taggedCorpus)

    pickle.dump(taggedCorpus, open(corpusName + 'Sentences.pickle', 'wb'))


if __name__ == "__main__":
    createTaggedCorpus('train', '../../resources/FrenchTreebank/corpus-tagged-train')
    createTaggedCorpus('test', '../../resources/FrenchTreebank/corpus-tagged-test')
