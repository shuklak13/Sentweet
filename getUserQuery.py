import sys
sys.path.insert(0,"twitter")    #add to python's module search path
import twitter

world=1
murica=23424977

def getUserQuery():
    query="trends?"
    while query=="trends?":
        query=raw_input("What do you want to search on Twitter?\n(Type \"trends?\" for popular trends, or \"QUIT\" to quit) \n")
        
        if query=="QUIT":
            quit()

        if query=="trends?":
            world_trends = twitter.api.trends.place(_id=world)
            print "Worldwide trends:"
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

            murica_trends = twitter.api.trends.place(_id=murica)
            print "\nUS trends:"
            #retrieve the top 5 trends
            try:            
                murica_trends_list=[murica_trends[0]["trends"][z]["name"]
                       for z in range(0, 5)]
            #if there are fewer than 5 trends, just take all the trends
            except IndexError:  
                murica_trends_list=[murica_trends[0]["trends"][z]["name"]
                        for z in range(0, len(murica_trends[0]["trends"]))]
            for z in range(0,len(murica_trends_list)):
                try:
                    print murica_trends_list[z]
                except UnicodeEncodeError:
                    pass
            print
    return query