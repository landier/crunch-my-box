import pickle
import nltk
from nltk.tokenize import word_tokenize

# Tests
from nltk.corpus import brown
from nltk.tag import UnigramTagger
tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
t = brown.tagged_sents(categories='news')

# Training & Test set
trainingSet = pickle.load(open('../resources/trainSentences.pickle', 'rb'))
testSet = pickle.load(open('../resources/testSentences.pickle', 'rb'))

# Functions
def evaluate(nameTagger, tagger):
    print nameTagger + ': ' + str(tagger.evaluate(testSet))

# Taggers
t1 = nltk.DefaultTagger('N')
t2 = nltk.UnigramTagger(trainingSet)
t3 = nltk.BigramTagger(trainingSet)
t4 = nltk.TrigramTagger(trainingSet)

t2t1 = nltk.UnigramTagger(trainingSet, backoff=t1)
t3t2 = nltk.BigramTagger(trainingSet, backoff=t2)
t4t3 = nltk.TrigramTagger(trainingSet, backoff=t3)

t3t2t1 = nltk.BigramTagger(trainingSet, backoff=t2t1)
t4t3t2 = nltk.TrigramTagger(trainingSet, backoff=t3t2)

t4t3t2t1 = nltk.TrigramTagger(trainingSet, backoff=t3t2t1)

# Evaluation
evaluate('t1', t1)
evaluate('t2', t2)
evaluate('t3', t3)
evaluate('t4', t4)
evaluate('t2t1', t2t1)
evaluate('t3t2', t3t2)
evaluate('t4t3', t4t3)
evaluate('t3t2t1', t3t2t1)
evaluate('t4t3t2', t4t3t2)
evaluate('t4t3t2t1', t4t3t2t1)


# Brill tagger
from nltk.tag.brill import *
templates = [
         SymmetricProximateTokensTemplate(ProximateTagsRule, (1,1)),
         SymmetricProximateTokensTemplate(ProximateTagsRule, (2,2)),
         SymmetricProximateTokensTemplate(ProximateTagsRule, (1,2)),
         SymmetricProximateTokensTemplate(ProximateTagsRule, (1,3)),
         SymmetricProximateTokensTemplate(ProximateWordsRule, (1,1)),
         SymmetricProximateTokensTemplate(ProximateWordsRule, (2,2)),
         SymmetricProximateTokensTemplate(ProximateWordsRule, (1,2)),
         SymmetricProximateTokensTemplate(ProximateWordsRule, (1,3)),
         ProximateTokensTemplate(ProximateTagsRule, (-1, -1), (1,1)),
         ProximateTokensTemplate(ProximateWordsRule, (-1, -1), (1,1)),
         ]
trainer = FastBrillTaggerTrainer(initial_tagger=t2, templates=templates, trace=3, deterministic=True)
brill_tagger = trainer.train(trainingSet, max_rules=10)

evaluate('Brill tagger', brill_tagger)