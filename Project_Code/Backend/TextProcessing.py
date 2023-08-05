from geopy.geocoders import Nominatim

from Backend.MachineLearningModel import SentimentAnalysis 
from Backend.TweetScraper import CollectTweets
from Backend.TextData import TwitterData

import pandas as pd
import spacy
import re
import csv

class DataProcessor:
    def __init__(self):
        # Initialise all apis & other stuff
        self.__nlp = spacy.load("en_core_web_sm")
        self.analysis = SentimentAnalysis()

    # Create object of TwitterData class to store data
    def _storeData(self, sentiment, text):
        twitterObject = TwitterData(sentiment=sentiment, text=text)
        return twitterObject

    # Reduce the tweet to bare text - remove everything else e.g. punctuation, numbers etc.
    def cleanTweet(self, text, lemmatise):
        temp = text.lower()
        
        # Followed part of this article - https://catriscode.com/2021/05/01/tweets-cleaning-with-python/ 
        # Removing hashtags and mentions
        temp = re.sub("@[A-za-z0-9_]+", "", temp)
        temp = re.sub("#[A-za-z0-9_]+", "", temp)

        # Removing links
        temp = re.sub(r"http\S+", "", temp)
        temp = re.sub(r"www.\S+", "", temp)

        temp = re.sub("'s", "", temp) # Get rid of possesive apostrophes         
        temp = self._decontract(temp) # Decontract contracted words

        # Removes all characters that aren't letters or whitespace
        temp = re.sub('[^A-Za-z ]+', '', temp)
        
        if lemmatise:
            temp = self._lemmatize(temp)

        return temp
    
    # Decontracts words eg won't -> will not etc.
    def _decontract(self, text):
        # specific
        text = re.sub(r"won\'t", "will not", text)
        text = re.sub(r"can\'t", "can not", text)

        # general
        text = re.sub(r"n\'t", " not", text)
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"\'d", " would", text)
        text = re.sub(r"\'ll", " will", text)
        text = re.sub(r"\'t", " not", text)
        text = re.sub(r"\'ve", " have", text)
        text = re.sub(r"\'m", " am", text)

        return text

    # Finds the root of the word
    def _lemmatize(self, text):
        doc = self.__nlp(text)
        finalDoc = ""

        for token in doc:
            finalDoc += token.lemma_ + ' '

        return finalDoc

# Subclass of DataProcessor
class TrainAlgorithm(DataProcessor):
    def __init__(self):
        super().__init__()

    # Prepares the data from the .csv file so it can be used to train the ML model
    def preprocessText(self, filepath):
        tweetData = []
        rawTweets = pd.read_csv(filepath)
        tweets = rawTweets.drop(columns=["From-User-Id", "To-User-Id", "Language", "Retweet-Count", "PartyName", "Id", 
        "Negativity", "Positivity", "Uncovered Tokens", "Total Tokens"]) # Removes the uneeded columns

        tweets.dropna(axis=0, inplace=True)  # Deletes items with empty cells

        newText = []

        for index in tweets.index:
            newText.append(self.cleanTweet(tweets['Scoring String'][index], False))

        # Creates a new column in the dataframe and adds the cleaned text to it
        tweets['clean_text'] = newText  

        # Creates an instance of the text class to store all relavent data
        for index in tweets.index:
            tweetSenti = self.__getSentiment(tweets['Score'][index])
            tweetText = tweets['clean_text'][index]           
            tweetData.append(self._storeData(tweetSenti, tweetText))

        # Exports to .csv file to see if the data has been manipulated correctly
        tweets.to_csv("CSV_Files/test.csv")

        # The file paths that the ML and vectorizer models will be stored at
        modelPath = 'Models/political_election_tweets_NB_test.pickle'
        vectModelPath ='Models/political_election_tweets_vect_test.pickle'

        # Train the model using the data from the .csv file
        self.analysis.trainModels(tweetData, modelPath, vectModelPath)

    # Get the sentiment based on the score given by the .csv file
    def __getSentiment(self, score):
        sentiment = None

        if score > 0:
            sentiment = 'positive'
        else:
            sentiment = 'negative'

        return sentiment

    # Call the function stored in its parent class
    def _storeData(self, sentiment, text):
        return super()._storeData(sentiment, text)

    # Call the function stored in its parent class
    def cleanTweet(self, tweet, lemmatise):
        return super().cleanTweet(tweet, lemmatise)

# Subclass of DataProcessor
class GatherTweetData(DataProcessor):
    def __init__(self, numOfTweets):
        super().__init__()
        self.__maxTweets = numOfTweets
        self.__geoLocator = Nominatim(user_agent="NEA_Project")
        self.__tweetCollecter = CollectTweets(self.__maxTweets)

    # Used for testing
    def testTweets(self):
        # Collects small number of tweets
        testTweetsDems = self.__tweetCollecter.searchDemocratTweets()
        testTweetsReps = self.__tweetCollecter.searchRepublicanTweets()
        tweetsDems = self.__organiseData(testTweetsDems)
        tweetsReps = self.__organiseData(testTweetsReps)

        # Writes the text data to a .txt file
        with open(r'Project_Code/tweets.txt', 'w') as f:
            f.write("DEMOCRATS\n\n")
            for tweet in tweetsDems:
                f.write(f"{tweet['text']}\n// \n")
            f.write("REPUBLICANS\n\n")
            for tweet in tweetsReps:
                f.write(f"{tweet['text']}\n// \n")

    # Gets the tweets that have been collected, finds the rest of the data such as polarity & 
    # location before exporting it to a .csv file
    def getTweets(self):
        # Searches for tweets
        repubData = self.__tweetCollecter.searchRepublicanTweets()
        demData = self.__tweetCollecter.searchDemocratTweets()

        # Adds the data to a big dictionary
        repubDict = self.__organiseData(repubData)
        demDict = self.__organiseData(demData)

        # Gets rid of all characters apart from text
        repubDict = self.cleanTweet(True, repubDict)
        demDict = self.cleanTweet(True, demDict)

        # Gets the senitment using trained ML and vectorizer models
        repubDict = self.__getSentiment(repubDict, 'Models/political_election_tweets_NB.pickle', 
        'Models/political_election_tweets_vect.pickle')
        demDict = self.__getSentiment(demDict, 'Models/political_election_tweets_NB.pickle', 
        'Models/political_election_tweets_vect.pickle')

        # List of TwitterData objects
        repubObjList = []
        demObjList = []

        
        # Finds location, assigns what party the tweet menitons and 
        # Creates TwitterData object of it before appending to a list
        for object in repubDict:
            object['republican'] = True
            object['location'] = self.__getLocation(object['location'])
            repubObjList.append(self.createTwitterObj(object))

        for object in demDict:
            object['republican'] = False
            object['location'] = self.__getLocation(object['location'])
            demObjList.append(self.createTwitterObj(object))

        # Combines the party's lists/dictionaries to a combined one
        tweetObjDict = repubDict + demDict # This is used to create a dataframe
        tweetObjList = repubObjList + demObjList

        # Creates dataframe so it can be easily exported to a .csv file
        df = pd.DataFrame(tweetObjDict)
        df.to_csv('twitter_obj.csv', mode='a', index=False, header=False)

        return tweetObjList

    # Gets the data from the .csv file
    def csvToListOfData(self):
        twitterObjList = []
        with open('twitter_data_no_duplicates.csv') as f:
            reader = csv.DictReader(f)
            lst = list(reader) # Converts the .csv to a list

            # Creates TwitterData object and appends to list
            for object in lst:
                twitterObjList.append(self.createTwitterObj(object))

        return twitterObjList

    # Gets polarity of all tweets and adds them to the dictionary
    def __getSentiment(self, twitterList, modelPath, vectPath):
        for tweet in twitterList:
            tempTextList = [] # The vectoriser only takes lists, not strings
            tempTextList.append(tweet['text'])
            tweet['sentiment'] = self.analysis.predictPolarity(tempTextList, modelPath, vectPath)

        return twitterList

    # Removes unnecessary characters from the text and lemmatises it
    # Calls its parent function
    def cleanTweet(self, lemmatise, twitterList):
        for tweet in twitterList:
            cleanText = super().cleanTweet(tweet['text'], lemmatise)
            tweet['clean_text'] = cleanText
        
        return twitterList

    # Creates a class to store all the data
    def createTwitterObj(self, data): #id=data['id']
        twitterObj = TwitterData(data['text'], loc=data['location'], creationDate=data['created_at'], 
        username=data['username'], lang=data['lang'], tweetMetrics=data['metrics'], 
        cleanText=data['clean_text'], sentiment=data['sentiment'], republican=data['republican'], 
        userMetrics=data['user_metrics'], key=int(data['id']))
        
        return twitterObj


    # Finds the state the user is situated in, if available
    def __getLocation(self, loc):
        # The state is always the second to last item
        state = None
        location = self.__geoLocator.geocode(loc, addressdetails=True)
        print(type(location))

        try:            
            country = location.address.split(',')[-1]
            tweetState = location.raw['address']['state']

            if country == ' United States':
                state = tweetState

        except KeyError:
            state = 'US'  # If the user hasn't specified the state they live in but they live in the US, 
                          # Location will be set to the US

        except:
            state = None

        return state

    # Sorts all the data into a single dict 
    def __organiseData(self, data):
        twitterDataList = []
        userData = data[0] # List of dictionaries
        tweetData = data[1]

        for i in range(len(userData)):
            userTweetData = {}

            userTweetData['username'] = userData[i]['username'] 
            userTweetData['user_metrics'] = userData[i]['user_metrics']
            userTweetData['location'] = userData[i]['location']

            userTweetData['text'] = tweetData[i]['text']
            userTweetData['created_at'] = tweetData[i]['time_created']
            #userTweetData['id'] = str(tweetData[i]['id'])
            userTweetData['key'] = tweetData[i]['key']
            userTweetData['lang'] = tweetData[i]['lang']
            userTweetData['metrics'] = tweetData[i]['metrics']
            userTweetData['republican'] = False
            userTweetData['clean_text'] = None
            userTweetData['sentiment'] = None 

            twitterDataList.append(userTweetData)

        return twitterDataList    



