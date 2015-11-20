

print "Booting up SentweetSearch..."

import twitter
#from collections import Counter
#from prettytable import PrettyTable
import json
from nltk.corpus import stopwords
import time
from nltk.classify import NaiveBayesClassifier
import nltk
#import thread

import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns

from pylab import *


#TRAINING STARTS HERE

posCorpus = open("TwitterAppCorpus/finalPositiveCorpus.txt", "r")
negCorpus = open("TwitterAppCorpus/finalNegativeCorpus.txt", "r")


stopWords = dict([(word, True) for word in stopwords.words('english')]) #nltk's stopwords
stopWords2 = [".","!","?","rt","@","=","+","-","&amp;","…","follow","i'm","i'll"] #my own set of stopwords

#INSERT TRAINING HERE

print "Determining polarity of features..."

def word_features(corpus):
    features = dict()
    x=0
    for line in corpus:
        x=x+1
        features.update([(word, True) for word in line.split() if word not in stopWords and word not in stopWords2])#features minus stopwords
#        if x==845: # this is to ensure balance between the positive and negative corpora
#            break
    return features

negfeats = (word_features(negCorpus), 'neg')
posfeats = (word_features(posCorpus), 'pos')

print "Establishing training set..."

trainfeats=[negfeats,posfeats]

print "Training the Naive Bayes Classifier..."

classifier = NaiveBayesClassifier.train(trainfeats)

#TRAINING ENDS HERE


#GENERATE THIS STUFF USING THE TWITTER WEBSITE
#CONSUMER_KEY=
#CONSUMER_SECRET=
#OAUTH_TOKEN=
#OAUTH_TOKEN_SECRET=

auth=twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter.api = twitter.Twitter(auth=auth)

#ID of the world, america, and dfw
world=1
murica=23424977
dfw=2388929 #DFW id is probably wrong, using the DFW geocode instead

#coordinates of dallas
dalLat=32.8029
dalLong=-96.7699
dalGeoCode=str(dalLat)+","+str(dalLong)+",60mi"

#These are the coordinates the program will search tweets in
locLat=0
locLong=0


def mergesort(x):
    result = []
    if len(x) < 2:
        return x
    mid = int(len(x)/2)
    y = mergesort(x[:mid])
    z = mergesort(x[mid:])
    while (len(y) > 0) or (len(z) > 0):
        if len(y) > 0 and len(z) > 0:
            if y[0]['retweet_count'] > z[0]['retweet_count']:
                result.append(z[0])
                z.pop(0)
            else:
                result.append(y[0])
                y.pop(0)
        elif len(z) > 0:
            for i in z:
                result.append(i)
                z.pop(0)
        else:
            for i in y:
                result.append(i)
                y.pop(0)
    return result


#trends
world_trends = twitter.api.trends.place(_id=world)

try:
    world_trends_list=[world_trends[0]["trends"][z]["name"]
                   for z in range(0, 5)]
except IndexError:
    world_trends_list=[world_trends[0]["trends"][z]["name"]
                   for z in range(0, len(world_trends[0]["trends"]))]

murica_trends = twitter.api.trends.place(_id=murica)
try:
    murica_trends_list=[murica_trends[0]["trends"][z]["name"]
                   for z in range(0, 5)]
except IndexError:
    murica_trends_list=[murica_trends[0]["trends"][z]["name"]
                   for z in range(0, len(murica_trends[0]["trends"]))]


#Program starts here

print "\n\nHello! Welcome to SentweetSeach!\n"


while True: #repeat forever!

    q="trends?"
    
    while q=="trends?":
        q=raw_input("What do you want to search on Twitter? (Type \"trends?\" for popular trends) \n")
        
        #if the user requests to see trends
        if q=="trends?":
            print "Worldwide trends:"
            for z in range(0,len(world_trends_list)):
                print world_trends_list[z]
            print
            print "US trends:"
            for z in range(0,len(murica_trends_list)):
                print murica_trends_list[z]
            print


    #these are choices the user makes
    variableChoice=0 #1 is location, 2 is day of week
    locationChoice=0 #1 is dfw, 2 is us, 3 is world
    dayChoice=-1 #0-6, this is the # of the day the user is searching
    dayOfWeek="" #Sun-Sat, this is the day the user is searching

    dayDiff=0 #todayNumber - DayChoice
    
    todayNumber=0 #1-7, this is the # of today
    todayOfWeek="" #Sun-Sat, this is today
    todayDay=0 #the date, excluding month and year
    todayDate="__________" #today's date

    searchDay=0
    strSearchDay=""
    searchDate="__________"
    
    searchMonth="" #month we are searching in
    lastDayOfMonth=0  #final day of searchMonth (31 for March, 30 for April, etc)
    searchYear=""

    timeChoice=0

            
    while variableChoice not in range(1,4):
        print "What do you want to search by?"
        print "\t1)Location"
        print "\t2)Day of Week"
        print "\t3)Time of Day"
        variableChoice = input("")
        if variableChoice not in range(1,4):
            print "Enter 1 or 2 to select a variable."

        #location search
        elif variableChoice==1:    
            while locationChoice not in range(1,4):
                print "Where do you want to search for tweets? (Includes retweets from outside locations)"
                print "\t1)The Dallas Fort Worth Area"
                print "\t2)The United States"
                locationChoice = input("\t3)The world\n")
                if locationChoice not in range(1,4):
                    print "Enter 1, 2, or 3 to select a location."

        #day search
        elif variableChoice==2:

            daysOfWeek=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
            
            while dayChoice not in range(0,7):
                print "From which day do you want to search for tweets?"
                for dai in range(0,7):
                    print str(dai+1)+")"+daysOfWeek[dai]
                dayChoice=int(input(""))-1
                if dayChoice not in range(0,7):
                    print "Enter a number 1-7 to select a day."
            dayOfWeek=daysOfWeek[dayChoice]
            #The date must be formatted YYYY-MM-DD
            todayDate = time.strftime("%Y-%m-%d")
            todayDay = int(time.strftime("%d"))
            todayOfWeek = time.strftime("%a")
            searchMonth = time.strftime("%m")
            searchYear = time.strftime("%Y")
            todayNumber = int(time.strftime("%w"))+1 #add one to make the scale 1-7, same scale as
                                                #dayChoice, rather than the default 0-6
            
            dayDiff = todayNumber-dayChoice #calculates the difference between today's date and
                                            #the date that the program will search for.
            if dayDiff<0:                   
                dayDiff=dayDiff+7           
            searchDay = todayDay-dayDiff +1    #searchDay is the day we will recieve tweets from.
                                        #I don't know why we need the +1 to make it work, but we do

            if searchDay<1:
                if searchMonth == 1:
                    searchMonth = 12
                    searchYear = str(int(searchYear)-1) #if rollback occurs on December,
                                                        #go to previous year
                elif searchMonth >= 11:
                    searchMonth = str(int(searchMonth)-1)
                elif searchMonth <= 10:
                    searchMonth = "0"+str(int(searchMonth)-1)

                if searchMonth=="01" or searchMonth=="03" or searchMonth=="05" or searchMonth=="07" or searchMonth=="08" or searchMonth=="10" or searchMonth=="12":
                    lastDayOfMonth = 31
                elif searchMonth=="02":
                    lastDayOfMonth = 28
                elif searchMonth=="04" or searchMonth=="06" or searchMonth=="09" or searchMonth=="11":
                    lastDayOfMonth = 30


            if searchDay >= 10:
                strSearchDay = str(searchDay)
            elif searchDay <= 9: #strSearchDay must be two-digits, so an extra 0 is necessary
                strSearchDay = "0" + str(searchDay)
                
            searchDate = searchYear + "-" + searchMonth + "-" + strSearchDay
            searchDate = searchYear + "-" + searchMonth + "-" + str(int(strSearchDay)+1)
            printSearchDate = searchYear + "-" + searchMonth + "-" + str(int(strSearchDay))

            print "Today's date is " + time.strftime("%Y-%m-%d, %a")+". You will be searching from "+printSearchDate+", "+dayOfWeek+"."


        #time search
        elif variableChoice==3:
            while timeChoice not in range(1,5):
                print "From what time do you want to search for tweets?"
                print "\t1)Morning (5AM-12PM)"
                print "\t2)Afternoon (12PM-5PM)"
                print "\t3)Evening (5PM-9PM)"
                print "\t4)Night (9PM-5AM)"
                timeChoice = input("")
                if timeChoice not in range(1,5):
                    print "Enter a number 1-5 to select a time of day."

                timeAfter2=25 #because 25 is outside of the time range of 0-24, it will never occur
                timeBefore2=25
                    
                if timeChoice == 1:
                    timeAfter=5
                    timeBefore=12
                if timeChoice == 2:
                    timeAfter=12
                    timeBefore=17
                if timeChoice == 3:
                    timeAfter=17
                    timeBefore=21
                if timeChoice == 4:
                    #Because Night streteches over two days, we must check separately if a tweets has
                    #been made between 9-12PM or 12-5AM
                    timeAfter=21
                    timeBefore=24
                    timeAfter2=0
                    timeBefore2=5

    
    while True:
        try:
            num=int(raw_input("How many tweets do you want to search?\n"))
            break
        except ValueError:
            print "\nPlease input an integer number."

    unlistedTweets=[]
    unlistedTweetsDFW=[]
    unlistedTweetsUS=[]
    unlistedTweetsWorld=[]
    
    lastID=max
    
    if variableChoice==1:
        #this is my old (not necessarily outdated) code
        if locationChoice==1:
            print "Searching the Dallas Fort Worth Area..."
            for i in range(0,5):
                search_results = twitter.api.search.tweets(q=q,lang="en",geocode=dalGeoCode,count=100,max_id=lastID)
                unlistedTweets = unlistedTweets+search_results['statuses'][:100]
                lastID = unlistedTweets[len(unlistedTweets)-1]["id"]
        if locationChoice==2:
            print "Searching the United States..."
            search=murica #search location
        if locationChoice==3:
            print "Searching the world..."
            search=world
        if locationChoice==2 or locationChoice==3:
            for i in range(0,5):
                search_results = twitter.api.search.tweets(q=q,lang="en",place=search,count=100,max_id=lastID)
                unlistedTweets = unlistedTweets+search_results['statuses'][:100]
                try:
                    lastID = unlistedTweetsWorld[len(unlistedTweets)-1]["id"]
                except IndexError:
                    lastID=lastID
        #this is my new code
        for i in range(0,10):
                search_resultsDFW = twitter.api.search.tweets(q=q,lang="en",geocode=dalGeoCode,count=100,max_id=lastID)
                unlistedTweetsDFW = unlistedTweetsDFW+search_resultsDFW['statuses'][:100]
                try:
                    lastID = unlistedTweetsWorld[len(unlistedTweetsDFW)-1]["id"]
                except IndexError:
                    lastID=lastID
        for i in range(0,10):
                search_resultsUS = twitter.api.search.tweets(q=q,lang="en",place=murica,count=100,max_id=lastID)
                unlistedTweetsUS = unlistedTweetsUS+search_resultsUS['statuses'][:100]
                try:
                    lastID = unlistedTweetsWorld[len(unlistedTweetsUS)-1]["id"]
                except IndexError:
                    lastID=lastID
        for i in range(0,10):
                search_resultsWorld = twitter.api.search.tweets(q=q,lang="en",place=world,count=100,max_id=lastID)
                unlistedTweetsWorld = unlistedTweetsWorld+search_resultsWorld['statuses']
                try:
                    lastID = unlistedTweetsWorld[len(unlistedTweetsWorld)-1]["id"]
                except IndexError:
                    lastID=lastID
    #location portion ends here

    elif variableChoice==2:
        print "Searching tweets from "+dayOfWeek+"..."
        for i in range(0,10):
            search_results = twitter.api.search.tweets(q=q,lang="en",place=world,count=100,until=searchDate,max_id=lastID)
            unlistedTweets = unlistedTweets+search_results['statuses'][:100]
            try:
                lastID = unlistedTweetsWorld[len(unlistedTweets)-1]["id"]
            except IndexError:
                lastID=lastID
            
    elif variableChoice==3:
        print "Searching tweets between "+str(timeAfter)+":00 and "+str(timeBefore)+":00..."
        for i in range(0,10):
            search_results = twitter.api.search.tweets(q=q,lang="en",place=murica,count=100,max_id=lastID)
            unlistedTweets = unlistedTweets+search_results['statuses'][:100]
            try:
                lastID = unlistedTweetsWorld[len(unlistedTweets)-1]["id"]
            except IndexError:
                lastID=lastID

    
                
    listOfTweets=[]
    listOfTweetsDFW=[]
    listOfTweetsUS=[]
    listOfTweetsWorld=[]

    x=0
    y=0

    print "Okay... loading...\n"

    try:
        while y<num:
            #if searching by location. Invalid tweets are already filtered out in search results
            if variableChoice==1:
                y=y+1
                listOfTweets.append(unlistedTweets[y])
                listOfTweetsDFW.append(unlistedTweetsDFW[y])
                listOfTweetsUS.append(unlistedTweetsUS[y])
                listOfTweetsWorld.append(unlistedTweetsWorld[y])
                        
            #if searching by day of week. All tweets from days not relevant are discarded.
            #[0:4] is first three letters of the day, and is used for comparision
            elif variableChoice==2:
                x=x+1
                if unlistedTweets[x]["created_at"][0:3] == dayOfWeek:
                    y=y+1
                    listOfTweets.append(unlistedTweets[x])
                    
            elif variableChoice==3:
                x=x+1
                if timeAfter <= int(unlistedTweets[x]["created_at"][11:13]) or timeAfter2 <= int(unlistedTweets[x]["created_at"][11:13]):
                    if int(unlistedTweets[x]["created_at"][11:13]) <= timeBefore or int(unlistedTweets[x]["created_at"][11:13]) <= timeBefore2:
                        y=y+1
                        listOfTweets.append(unlistedTweets[x])

    except IndexError:
        print "We were not able to find "+str(num)+" tweets about "+q+". Sorry."        

    orderedListOfTweets=mergesort(listOfTweets)
    orderedListOfTweets.reverse()

    try:
        mostRetweeted=orderedListOfTweets[0]
    except IndexError:
        print ""

    orderedListOfTweetsDFW=mergesort(listOfTweetsDFW)
    orderedListOfTweetsDFW.reverse()
    
    orderedListOfTweetsUS=mergesort(listOfTweetsUS)
    orderedListOfTweetsUS.reverse()
    
    orderedListOfTweetsWorld=mergesort(listOfTweetsWorld)
    orderedListOfTweetsWorld.reverse()
    
    numPos=0
    numNeg=0
    
    numPosDFW=0
    numNegDFW=0
    
    numPosUS=0
    numNegUS=0
    
    numPosWorld=0
    numNegWorld=0

    
    for z in range (0, len(orderedListOfTweets)):
            
        place=orderedListOfTweets[z]["user"]["location"]
        person=orderedListOfTweets[z]["user"]["screen_name"]
        numRetweets=orderedListOfTweets[z]["retweet_count"]
        geocode=orderedListOfTweets[z]["geo"]

        print str(z+1) + ") " + person + ": "+ orderedListOfTweets[z]['text']
        print "(Retweeted "+str(numRetweets)+" times)"
        if orderedListOfTweets[z]["user"]["location"]=="":
            print "(Location unknown)."
        else:
            print "(Tweeted from "+place+")."
        print "(Tweeted on "+orderedListOfTweets[z]["created_at"].split(" +")[0]+")"

        if classifier.classify(dict([(word, True) for word in orderedListOfTweets[z]['text'].split()])) == 'neg':
            print "(Detected a negative sentiment)"
            numNeg=numNeg+1
        if classifier.classify(dict([(word, True) for word in orderedListOfTweets[z]['text'].split()])) == 'pos':
            print "(Detected a positive sentiment)"
            numPos=numPos+1
        print

#this counts the sentiment of the location tweets
    if variableChoice==1:
        if locationChoice==1:
            numPosDFW=numPos
            numNegDFW=numNeg
        else:
            for z in range(0,len(orderedListOfTweetsDFW)):
                if classifier.classify(dict([(word, True) for word in orderedListOfTweetsDFW[z]['text'].split()])) == 'neg':
                    numNegDFW=numNegDFW+1
                if classifier.classify(dict([(word, True) for word in orderedListOfTweetsDFW[z]['text'].split()])) == 'pos':
                    numPosDFW=numPosDFW+1
        if locationChoice==2:
            numPosUS=numPos
            numNegUS=numNeg
        else:
            for z in range(0,len(orderedListOfTweetsUS)):
                if classifier.classify(dict([(word, True) for word in orderedListOfTweetsUS[z]['text'].split()])) == 'neg':
                    numNegUS=numNegUS+1
                if classifier.classify(dict([(word, True) for word in orderedListOfTweetsUS[z]['text'].split()])) == 'pos':
                    numPosUS=numPosUS+1
        if locationChoice==1:
            numPosWorld=numPos
            numNegWorld=numNeg
        else:
            for z in range(0,len(orderedListOfTweetsWorld)):
                if classifier.classify(dict([(word, True) for word in orderedListOfTweetsWorld[z]['text'].split()])) == 'neg':
                    numNegWorld=numNegWorld+1
                if classifier.classify(dict([(word, True) for word in orderedListOfTweetsWorld[z]['text'].split()])) == 'pos':
                    numPosWorld=numPosWorld+1


        print "In your search, found " + str(numPos) + " positive tweets, and " + str(numNeg) + " negative ones."
        print "In DFW, found " + str(numPosDFW) + " positive tweets, and " + str(numNegDFW) + " negative ones."
        print "In US, found " + str(numPosUS) + " positive tweets, and " + str(numNegUS) + " negative ones."
        print "In World, found " + str(numPosWorld) + " positive tweets, and " + str(numNegWorld) + " negative ones."


    else:
        print "In your search, found " + str(numPos) + " positive tweets, and " + str(numNeg) + " negative ones."

    
    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1, 0.8, 0.8])
    labels = 'Positive', 'Negative'

    try:
        fracPos=numPos*100/(numPos+numNeg)
        fracNeg=numNeg*100/(numPos+numNeg)
    except ZeroDivisionError:
        print "No tweets were found. Sorry."

##    print fracPos
##    print fracNeg
    
    fracs = [fracPos, fracNeg]
    explode=(0.05, 0.05)

    pie(fracs, explode=explode, labels=labels, shadow=True, autopct='%1.1f%%')

    variableOfChoice=""

    if variableChoice==1:
        if locationChoice==1:
            location="DFW Area"
        if locationChoice==2:
            location="The US"
        if locationChoice==3:
            location="The World"
        variableOfChoice=="Location ("+location+")"
    if variableChoice==2:
        variableOfChoice=="Day of the Week, ("+dayOfWeek+")"
    if variableChoice==3:
        variableOfChoice=="Time of Day"

    title('Positive vs. Negative \nSentiment Distribution of Tweets for '+q, bbox={'facecolor':'0.8', 'pad':5})

    show()

##        for i in range(0,10):
##            search_results = twitter.api.search.tweets(q=q,lang="en",place=world,count=100,until=searchDate,max_id=lastID)
##            unlistedTweets = unlistedTweets+search_results['statuses'][:100]
##            lastID = unlistedTweets[len(unlistedTweets)-1]["id"]
##        
##        for z in range(0,len(orderedListOfTweetsWorld)):
##                if classifier.classify(dict([(word, True) for word in orderedListOfTweetsWorld[z]['text'].split()])) == 'neg':
##                    numNegWorld=numNegWorld+1
##                if classifier.classify(dict([(word, True) for word in orderedListOfTweetsWorld[z]['text'].split()])) == 'pos':
##                    numPosWorld=numPosWorld+1


##    if variableChoice==1: #I only have tables display if search by location right now
##    
##        status_texts = [tweet['text']
##                        for tweet in unlistedTweets]
##        screen_names = [user_mention['screen_name']
##                        for tweet in unlistedTweets 
##                        for user_mention in tweet['entities']['user_mentions']]
##        hashtags = [hashtag['text'].lower()
##                     for tweet in unlistedTweets
##                     for hashtag in tweet['entities']['hashtags']]
##        words = [w.lower()
##                 for t in status_texts
##                 for w in t.split()
##                 if w.lower() not in stopWords
##                 if w.lower() not in stopWords2]
##
##        
##        #display most common words, screen names, and hashtags in a "pretty table"
##        for label, data in (('Words',words),('Screen Name',screen_names),('Hashtags',hashtags)):
##            pt=PrettyTable(field_names=[label,'Count'])
##            c=Counter(data)
##            [pt.add_row(kv) for kv in c.most_common()[:15]]
##            pt.align[label],pt.align['Count']='l','r', #align first column to left and second to right
##            print pt
##
##        retweets=[(status['retweet_count'],
##                   status['retweeted_status']['user']['screen_name'],
##                   status['text'])
##                  for status in orderedListOfTweets
##                      if status.has_key('retweeted_status')]
##
##        pt=PrettyTable(field_names=['Retweet Count','Screen Name','Text'])
##        [pt.add_row(row) for row in sorted(retweets,reverse=True)[:5]]
##        pt.max_width['Text']=50
##        pt.align='l'
##        print pt


    break
    _ = raw_input("\nPress enter to search again.")
