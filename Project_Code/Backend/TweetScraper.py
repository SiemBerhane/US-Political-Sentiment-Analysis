import tweepy

class CollectTweets:
    def __init__(self, maxTweets):
        # Authorise API
        # The password has been censored
        self.__client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAPORgQEAAAAA7ZcWW75MRdpMYlZPDh6IHKlzQ1w%3DQBM7812mKRQVghVoJSjvk50aVIrewDLQHqdICx41WI8Si8ChLL")
        self.__MAX_TWEETS = maxTweets

        # Get tweets in English mentioning only one of the parties from a US based user that isn't a retweet
        self.__REPUBLICAN_QUERY = "(republican OR republicans) lang:en -(democrat OR democrats) -is:retweet"
        self.__DEMOCRAT_QUERY = "(democrat OR democrats) lang:en -(republican OR republicans) -is:retweet"

    # Searches tweets and returns specified data
    def searchRepublicanTweets(self):
        # The data returned is in the form of a JSON file
        repubTweets = self.__client.search_recent_tweets(query=self.__REPUBLICAN_QUERY, tweet_fields=['created_at', 'text', 'id', 'lang', 'public_metrics'], 
        expansions='author_id', user_fields=['username', 'location', 'public_metrics'], max_results=self.__MAX_TWEETS)

        # Have to deal with user and tweet data seperately
        userData = self.__formatUserDetails(repubTweets.includes['users'])
        tweetData = self.__formatTweetDetails(repubTweets.data)

        return (userData, tweetData)

    # Same as searchRepublicanTweets
    def searchDemocratTweets(self):
        demTweets = self.__client.search_recent_tweets(query=self.__DEMOCRAT_QUERY, tweet_fields=['created_at', 'text', 'id', 'lang', 'public_metrics'], 
        expansions='author_id', user_fields=['username', 'location', 'public_metrics'], max_results=self.__MAX_TWEETS)

        userData = self.__formatUserDetails(demTweets.includes['users'])
        tweetData = self.__formatTweetDetails(demTweets.data)

        return (userData, tweetData)

    # Adds data to a dictionary
    def __formatUserDetails(self, userJSON):
        userDataList = []

        for user in userJSON:
            # Will contain the location, username and metrics of the user and their account
            userData = {} 

            userData['location'] = user['location']
            userData['username'] = user['username']
            userData['user_metrics'] = user['public_metrics']

            userDataList.append(userData)

        return userDataList # Returns a list of dictionaries

    # Adds data to a dictionary
    def __formatTweetDetails(self, tweetJSON):
        tweetDataList = []

        for tweet in tweetJSON:
            tweetData = {} # Will contain the text, time created at, tweet ID, 
            # language & metrics of the tweet

            tweetData['text'] = tweet['text']
            tweetData['time_created'] = tweet['created_at']
            tweetData['key'] = self.__getKey(tweet['id'])
            tweetData['lang'] = tweet['lang']
            tweetData['metrics'] = tweet['public_metrics']

            tweetDataList.append(tweetData)

        return tweetDataList # Returns a list of dictionaries

    # Returns the last 5 digits of the ID
    def __getKey(self, id):
            strId = str(id)
            key = strId[-5::]
            intKey = int(key)
            return intKey