import codecs, os, pickle
import xml.etree.ElementTree as etree

def createTaggedCorpus(name):
    inputDirectory = 'FrenchTreebank/corpus-tagged-' + name
    #outputFile = codecs.open(name + 'Sentences.txt', 'a', 'utf-8')

    files = os.listdir(inputDirectory)

    for file in files:
        tree = etree.parse(inputDirectory + '/' + file)
        root = tree.getroot()

        sentences = root.findall("SENT")
    
        taggedSentences = []
        for sentence in sentences:
            words = sentence.findall("w")

            taggedWords = []
            for word in words:
                try:
                    if word.text is None:
                        continue
                    elif len(word) > 0:
                        #print(word.attrib['lemma'] + '/' + word.attrib['cat'])
                        #outputFile.write(word.attrib['lemma'] + '/' + word.attrib['cat'] + ' ')
                        taggedWords.append((word.attrib['lemma'], word.attrib['cat']))
                    elif word.text is not None:
                        #print(word.text + '/' + word.attrib['cat'])
                        #outputFile.write(word.text + '/' + word.attrib['cat'] + ' ')
                        taggedWords.append((word.text, word.attrib['cat']))
                except:
                    print(file + " - " + etree.tostring(word))
                    pass

            taggedSentences.append(taggedWords)

    pickle.dump(taggedSentences, open(name + 'Sentences.pickle', 'wb'))

createTaggedCorpus('train')
createTaggedCorpus('test')
