import sys
sys.path.insert(0,"twitter")    #add to python's module search path
import twitter

world=1
murica=23424977

def getUserQuery():
    q="trends?"
    while q=="trends?":
        q=raw_input("What do you want to search on Twitter? (Type \"trends?\" for popular trends) \n")
        
        #if the user requests to see trends
        if q=="trends?":
            print "Worldwide trends:"
            world_trends = twitter.api.trends.place(_id=world)
            #retrieve top 5 trends
            try:
                world_trends_list=[world_trends[0]["trends"][z]["name"]
                       for z in range(0, 5)]
            #if there are fewer than 5 trends, just take all the trends
            except IndexError:
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
    return q