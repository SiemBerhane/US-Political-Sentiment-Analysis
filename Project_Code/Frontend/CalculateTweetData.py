import statistics

class CalculateTweetData:
    def __init__(self, sorting):
        self.sorting = sorting # The merge sort class

    # Gets the all the data to do with the datset that is currently displayed
    # Returns a dictionary of all the data which will be displayed
    def generalData(self, tweetList):
        # Finds num of +ve & -ve tweets to do with each party
        posTweets = self.__numOfPositveTweets(tweetList)
        negTweets = len(tweetList) - posTweets

        repubTweets = self.__numOfRepubTweets(tweetList)
        demTweets = len(tweetList) - repubTweets
        
        # Finds the percentage of all the values
        posPerc = self.__percentageOf(posTweets, len(tweetList))
        negPerc = self.__percentageOf(negTweets, len(tweetList))
        demPerc = self.__percentageOf(demTweets, len(tweetList))
        repubPerc = self.__percentageOf(repubTweets, len(tweetList))

        # Uses the statistics library to find the mean & median. Rounds to nearest whole number
        meanFollowers = round(statistics.mean(self.__followersList(tweetList)), 0)
        medianFollowers = round(statistics.median(self.__followersList(tweetList)), 0)
        
        # Uses merge sort algorithm to sort list from highest follower count to lowest
        followerSortedList = self.sorting.mergeSort(self.__followersList(tweetList), False)
        maxFollowers = followerSortedList[0] # Account with most followers will be first in the list
        minFollowers = followerSortedList[-1] # Account with least followers will be last in the list

        data = {
            'Number Of Positive Tweets:': posTweets,
            'Number Of Negative Tweets:': negTweets, 
            'Positive Tweets %:': posPerc,
            'Negative Tweets %:': negPerc,
            'Number of Republican Tweets:': repubTweets,
            'Republican Tweets %:': repubPerc,
            'Positive Republican Opinion, YouGov, 21/2/23: ': '44.3%',
            'Negative Republican Opinion, YouGov, 21/2/23: ':'52.9%',
            'Number of Democratic Tweets:': demTweets,
            'Democratic Tweets %:': demPerc,
            'Positive Democrat Opinion, YouGov, 21/2/23: ': '45.7%',
            'Negative Democrat Opinion, YouGov, 21/2/23: ': '52.1%',
            'Mean Number of Followers:': meanFollowers,
            'Median Number of Follwers:': medianFollowers,
            'Max Number of Followers:': maxFollowers,
            'Min Number of Followers:': minFollowers
        }

        return data


    # Gets the follower count from TwitterData instance of each tweet
    # And appends it to a list
    def __followersList(self, lst):
        followersList = []
        for obj in lst:
            followersList.append(int(obj.userMetrics['followers_count']))

        return followersList

    # Increases by 1 if the sentiment of the tweet is positive
    def __numOfPositveTweets(self, tweetList):
        num = 0
        for tweet in tweetList:
            if tweet.sentiment == 'positive':
                num += 1
        
        return num

    # Increases by 1 if the party mentioned is the Republicans
    def __numOfRepubTweets(self, tweetList):
        num = 0
        for tweet in tweetList:
            if tweet.repub == True:
                num += 1

        return num

    # Finds the % to 2 d.p.
    def __percentageOf(self, n1, n2):
        return round((n1/n2) * 100, 2)