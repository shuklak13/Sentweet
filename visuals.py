import sys
from collections import Counter, defaultdict
sys.path.insert(0,"prettytable")
from prettytable import PrettyTable
import matplotlib.pyplot as py  #pie graphs
from featureFunctions import stopWords
import random   #used to create random colors

def createTables(listOfTweets):
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
            if w.lower() not in stopWords]
    words = [w.lower()
            for t in status_texts
            for w in t.split()
            if w.lower() not in stopWords]

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

def createPieChart(numPos, numNeg, q):
    if numPos+numNeg>0:
        labels = "Positive", "Negative"
        fracs = [numPos, numNeg]
        explode=(0.05, 0.05)
        listOfColors = ['b','g','r','c','m','y']
        random.shuffle(listOfColors)    #random colors
        py.pie(fracs, explode=explode, labels=labels, shadow=True, autopct='%1.1f%%', colors=[listOfColors[0], listOfColors[1]])
        py.title('Positive vs. Negative \nSentiment Distribution of Tweets for ' + q, bbox={'facecolor':'0.8', 'pad':5})
        py.show()
        print "Close pie chart to continue\n"
    else:
        print "No tweets were found... Sorry!"