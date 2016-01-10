#To-do:
#	Turn into a proper package
#	trainClassifier.py
#		Measure accuracy
			# http://www.nltk.org/book/ch06.html
			# http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
			# http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
	#   Improve Sentiment Analysis
	#		movie sentiment analysis program
	#		other classification algorithms
	#		preprocessing, feature engineering
#   Add back the location feature

print "Booting up SentweetSearch..."

#the essentials
import sys
sys.path.insert(0,"twitter")	#add to python's module search path
import twitter

#visuals

#modules containing my functions
from unicodeFunctions import *
from trainClassifier import trainClassifier
from getUserQuery import getUserQuery
from twitterSearch import twitterSearch
import visuals

classifier = trainClassifier()

#GENERATE THIS STUFF USING THE TWITTER WEBSITE
#CONSUMER_KEY=
#CONSUMER_SECRET=
#OAUTH_TOKEN=
#OAUTH_TOKEN_SECRET=

auth=twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter.api = twitter.Twitter(auth=auth)

while True: #repeat forever!
    query = getUserQuery()

    searchResults = twitterSearch(query, classifier)
    listOfTweets = searchResults[0]
    numPos = searchResults[1]
    numNeg = searchResults[2]

    visuals.createTables(listOfTweets)
    visuals.createPieChart(numPos, numNeg, query)

    continueCheck = raw_input("\nPress enter to search again, or type 'q' to quit.\n")
    if continueCheck=="q":
    	break