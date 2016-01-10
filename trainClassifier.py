from nltk.classify import NaiveBayesClassifier
from nltk.classify import MaxentClassifier
from nltk.classify import DecisionTreeClassifier
from featureFunctions import *

def trainClassifier():
	print "Determining polarity of features..."

	#NLTK classifiers work on "featstructs", simple dictionaries
	    #mapping a feature name to a feature value
	    #We use booleans to indicate that the set (a tweet) does(n't) contain a keyword
	    #For more information: http://www.nltk.org/howto/featstruct.html

	#A tuple (dict, label)
	    #Where dict is a dictionary of (word, boolean) key-val pairs
	    #label indicates positive or negative
	posfeats = feature_tuple("finalPositiveCorpus.txt", "r", "pos")
	negfeats = feature_tuple("finalNegativeCorpus.txt", "r", "neg")

	# negcutoff = len(negfeats)*3/4
	# poscutoff = len(posfeats)*3/4

	# trainfeats = [negfeats[:negcutoff], posfeats[:poscutoff]]
	# testfeats = [negfeats[negcutoff:], posfeats[poscutoff:]]

	#a list of (dict, label) tuples, one for each label
	trainfeats=[negfeats,posfeats]

	#trainfeats = negfeats + posfeats

	print "Training the classifier..."

	#uses list of (dict, label) tuples to train classifier to identify each label
	classifier = NaiveBayesClassifier.train(trainfeats)
	# classifier = MaxentClassifier.train(trainfeats)   
	# classifier = DecisionTreeClassifier.train(trainfeats) 

	#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)

	#these features don't seem very good
	#obviously my classifier needs improvement
	#classifier.show_most_informative_features()

	return classifier