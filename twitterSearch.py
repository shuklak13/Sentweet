import sys
sys.path.insert(0,"twitter")	#add to python's module search path
import twitter
from unicodeFunctions import *
from featureFunctions import *

def twitterSearch(query, classifier):
	#get first 100 tweets
    #twitter.api.search.tweets() returns a dictionary
    listOfTweets = twitter.api.search.tweets(q = query,lang="en",count=100)["statuses"]

    print "Okay... loading...\n"
    
    numPos=0
    numNeg=0

    tweetNumber = 0 #used for output
    for tweet in listOfTweets:
        tweetNumber += 1
        place=utf8(tweet["user"]["location"])
        person=utf8(tweet["user"]["screen_name"])
        numRetweets=tweet["retweet_count"]
        geocode=tweet["geo"]
        time=tweet["created_at"].split(" +")[0]
        text=utf8(tweet['text'])

        print str(tweetNumber) + ") " + person + ": " + text
        print "(Retweeted "+str(numRetweets)+" times)"
        if place=="":
            print "(Location unknown)."
        else:
            print "(Tweeted from "+place+")."
        print "(Tweeted on "+time+")"

        tweetFeatures = extractFeaturesFrom(tweet["text"])
        if tweetFeatures is not None:
            polarity = classifier.classify(tweetFeatures)
            if polarity == "neg":
                print "(Detected a negative sentiment)"
                numNeg=numNeg+1
            elif polarity == "pos":
                print "(Detected a positive sentiment)"
                numPos=numPos+1
        print

    print "In your search, found " + str(numPos) + " positive tweets, and " + str(numNeg) + " negative ones."

    return (listOfTweets, numPos, numNeg)