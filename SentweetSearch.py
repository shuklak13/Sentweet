#To-do:
#	trainClassifier.py
	#   Improve Sentiment Analysis (currently positive-biased)
	#		http://marcobonzanini.com/2015/05/17/mining-twitter-data-with-python-part-6-sentiment-analysis-basics/
	#		movie sentiment analysis program
	#		other classification algorithms
	#		preprocessing, feature engineering
#   Add back the location feature

#"main method"
if __name__ == "__main__":

	print "Booting up SentweetSearch..."

	#the essentials
	import sys
	sys.path.insert(0,"twitter")	#add to python's module search path
	import twitter

	#modules containing my functions
	from unicodeFunctions import toUnicode, utf8
	from trainClassifier import trainClassifier
	from getUserQuery import getUserQuery
	from twitterSearch import twitterSearch
	import visuals

	classifier = trainClassifier()

	#GENERATE THIS STUFF USING THE TWITTER WEBSITE
	#If you need help, follow a tutorial:
		#https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/
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