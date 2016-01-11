#This script is based off of this:
#   http://www.nltk.org/book/ch06.html
#Unfortunately, NLTK's tutorial doesn't work because NaiveBayesClassifier requires a dictionary to be built
#But the tutorial wants you to make it a list (as shown in this script)

#I was going to use this script to find the accuracy of my classifier
    #but the official textbook's explanation doesn't seem to work.
#So this is on hiatus (indefinitely) until I can figure out how.

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
def normalize(word):
     return stemmer.stem(word.lower())

from unicodeFunctions import *
from nltk.corpus import stopwords
stopWords = dict([(word, True) for word in stopwords.words('english')]) #nltk's stopwords
stopWords2 = [".","!","?","rt","@","=","+","-","&amp;","follow","i'm","i'll"]
stopWords2 = dict([(toUnicode(word), True) for word in stopWords2]) #my own set of stopwords
stopWords.update(stopWords2)

from nltk.classify import NaiveBayesClassifier
from nltk.classify import MaxentClassifier
from nltk.classify import DecisionTreeClassifier
from nltk.classify.util import accuracy

def wordsInCorpus(corpus):
    words = list()
    for line in corpus:
        for word in line.split():
            if word not in stopWords:
                words.append(normalize(word))
    return words

posCorpus = open("finalPositiveCorpus.txt", "r")
poswords = wordsInCorpus(posCorpus)
negCorpus = open("finalNegativeCorpus.txt", "r")
negwords = wordsInCorpus(negCorpus)

#list of tuples (word, label) for every non-stop word that occurs in each corpus
labeled_features = ([(word, 'pos') for word in poswords] + [(word, 'neg') for word in negwords])

import random
random.shuffle(labeled_features)

cutOff = len(labeled_features) * 3/4

train_set, test_set = labeled_features[cutOff:], labeled_features[:cutOff]

#this is where the script crashes
#This WOULD work if NaiveBayesClassifier.train() worked on lists
#But it only works on dictionaries, contrary to what documentation says
classifier = NaiveBayesClassifier.train(train_set)  

print 'accuracy:', accuracy(classifier, test_set)