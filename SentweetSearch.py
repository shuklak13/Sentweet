#To-do:
#   Improve Sentiment Analysis
#   Add back the location feature

print "Booting up SentweetSearch..."

#imports and function declarations

#the essentials
import sys
sys.path.insert(0,"twitter")
import twitter

from collections import Counter, defaultdict
sys.path.insert(0,"prettytable")
from prettytable import PrettyTable

#nltk stuff
#Reasons for Naive Bayes:
    #Faster to train than Maximum Entropy, more accurate than Decision Tree
    #Naive assumption isn't too harmful because tweets are so small (fewer collocations)
    #My experience with Maximum Entropy gave me poor results
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
#from nltk.classify import MaxentClassifier
#from nltk.classify import DecisionTreeClassifier
from nltk.stem.porter import PorterStemmer
import nltk

#pie graphs
import matplotlib.pyplot as py

#See this link for unicode explanation (Specifically, read about "Unicode Sandwich")
    #http://nedbatchelder.com/text/unipain.html
#used to convert byte strings to unicode (used for inner workings)
def toUnicode(txt):
    return txt.decode("utf-8", errors='ignore')
def utf8(txt):
    return txt.encode(sys.stdout.encoding, errors='ignore')

stemmer = PorterStemmer()
#stems the word and lowercases it
def normalize(word):
     return stemmer.stem(word.lower())

#Code starts here

#TRAINING BEGINS HERE
stopWords = dict([(word, True) for word in stopwords.words('english')]) #nltk's stopwords
stopWords2 = [".","!","?","rt","@","=","+","-","&amp;","follow","i'm","i'll"] #my own set of stopwords
stopWords2 = [toUnicode(word) for word in stopWords2]

print "Determining polarity of features..."

#return tuple (features, label)
#for input into NLTK's Naive Bayes Classifier
def feature_tuple(fileName, mode, label):
    features = word_features(fileName, mode)
    return (features, label)

#add each word from the corpus into our dictionary
    #if it's not a stopword
#Note that normalization (word.lower()) is not needed 
    #because the Stanford corpus is already lowercase
#Other corpora might need to be normalized, however
def word_features(fileName, mode):
    corpus = open(fileName, mode)
    features = dict()
    for line in corpus:
        line = toUnicode(line)
        newFeatures = extractFeaturesFrom(line)
        if newFeatures is not None:  #if line is NoneType, skip to next line
            features.update(newFeatures)
    corpus.close()
    return features

#iterate through every word in text, normalize it, and remove stopwords
def extractFeaturesFrom(text):
    if text is not None:
        return dict([(normalize(word), True) for word in text.split() 
                    if word not in stopWords and word not in stopWords2])
    else:
        return None

#NLTK classifiers work on "featstructs", simple dictionaries
    #mapping a feature name to a feature value
    #We use booleans to indicate that the set (a tweet) does(n't) contain a keyword
    #For more information: http://www.nltk.org/howto/featstruct.html

#A tuple (dict, label)
    #Where dict is a dictionary of (word, boolean) key-val pairs
    #label indicates positive or negative
posfeats = feature_tuple("finalPositiveCorpus.txt", "r", "pos")
negfeats = feature_tuple("finalNegativeCorpus.txt", "r", "neg")

trainfeats=[negfeats,posfeats]

print "Training the Naive Bayes Classifier..."

classifier = NaiveBayesClassifier.train(trainfeats)
#classifier = MaxentClassifier.train(trainfeats)   
#classifier = DecisionTreeClassifier.train(trainfeats) 

#TRAINING ENDS HERE

#GENERATE THIS STUFF USING THE TWITTER WEBSITE
#CONSUMER_KEY=
#CONSUMER_SECRET=
#OAUTH_TOKEN=
#OAUTH_TOKEN_SECRET=

auth=twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter.api = twitter.Twitter(auth=auth)

world=1
murica=23424977

while True: #repeat forever!
    q="trends?"
    while q=="trends?":
        q=raw_input("What do you want to search on Twitter? (Type \"trends?\" for popular trends) \n")
        
        #if the user requests to see trends
        if q=="trends?":
            print "Worldwide trends:"
            world_trends = twitter.api.trends.place(_id=world)
            try:            #retrieve the top 5 trends
                world_trends_list=[world_trends[0]["trends"][z]["name"]
                       for z in range(0, 5)]
            except IndexError:  #if there are fewer than 5 trends, just take all the trends
                world_trends_list=[world_trends[0]["trends"][z]["name"]
                           for z in range(0, len(world_trends[0]["trends"]))]
            for z in range(0,len(world_trends_list)):
                try:
                    print world_trends_list[z]
                except UnicodeEncodeError:
                    pass

            print "\nUS trends:"
            murica_trends = twitter.api.trends.place(_id=murica)
            try:            #retrieve the top 5 trends
                murica_trends_list=[murica_trends[0]["trends"][z]["name"]
                       for z in range(0, 5)]
            except IndexError:  #if there are fewer than 5 trends, just take all the trends
                murica_trends_list=[murica_trends[0]["trends"][z]["name"]
                        for z in range(0, len(murica_trends[0]["trends"]))]
            for z in range(0,len(murica_trends_list)):
                try:
                    print murica_trends_list[z]
                except UnicodeEncodeError:
                    pass
            print

    lastID=max
    query = q
    #get first 100 tweets
    #twitter.api.search.tweets() returns a dictionary
    listOfTweets = twitter.api.search.tweets(q = q,lang="en",count=100)["statuses"]

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


    #pretty table
    status_texts = [tweet['text']
                   for tweet in listOfTweets]
    screen_names = [user_mention['screen_name']
                   for tweet in listOfTweets 
                   for user_mention in tweet['entities']['user_mentions']]
    hashtags = [hashtag['text'].lower()
                for tweet in listOfTweets
                for hashtag in tweet['entities']['hashtags']]
    words = [w.lower()
            for t in status_texts
            for w in t.split()
            if w.lower() not in stopWords
            if w.lower() not in stopWords2]
    words = [w.lower()
            for t in status_texts
            for w in t.split()
            if w.lower() not in stopWords
            if w.lower() not in stopWords2]
   
    #create tables displaying the most common words, users, and hashtags in our search
    for label, data in (('Most Common Words',words),('Most Common Users',screen_names),('Most Common Hashtags',hashtags)):
        pt=PrettyTable(field_names=[label,'Count'])
        c=Counter(data)
        [pt.add_row(kv) for kv in c.most_common()[:15]]
        pt.align[label],pt.align['Count']='l','r', #align first column to left, second to right
        print pt

    #table of most retweeted tweets
    retweets=[(status['retweet_count'],
              status['retweeted_status']['user']['screen_name'],
              status['text'])
        for status in listOfTweets
            if status.has_key('retweeted_status')]

    pt=PrettyTable(field_names=['Retweet Count','Screen Name','Text'])
    [pt.add_row(row) for row in sorted(retweets,reverse=True)[:5]]
    pt.max_width['Text']=50
    pt.align='l'
    print pt

    #pie chart
        #Works inconsistently - will fix in future release
    if numPos+numNeg>0:
        labels = "Positive", "Negative"
        fracs = [numPos, numNeg]
        explode=(0.05, 0.05)
        py.pie(fracs, explode=explode, labels=labels, shadow=True, autopct='%1.1f%%')
        py.title('Positive vs. Negative \nSentiment Distribution of Tweets for ' + q, bbox={'facecolor':'0.8', 'pad':5})
        py.show()
    else:
        print "No tweets were found... Sorry!"


    break
    _ = raw_input("\nPress enter to search again.")