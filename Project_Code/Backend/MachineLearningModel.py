from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle

class SentimentAnalysis:
    def __init__(self):
        self.__TRAINPERCENTAGE = 0.8
        
    # Gets the text from each tweet
    def __getListOfTweets(self, tweetData):
        text = []
        for tweet in tweetData:
            text.append(tweet.text)

        return text

    # Gets the sentiment from each of the tweets
    def __getListOfSentiments(self, tweetData):
        sentiment = []
        for tweet in tweetData:
            sentiment.append(tweet.sentiment)

        return sentiment

    # Trains and tests a machine learning and vectorization model
    def trainModels(self, data, modelPath, vectModelPath):
        NB = MultinomialNB()
        
        # Split into train and test data
        textData = self.__getListOfTweets(data)
        sentimentData = self.__getListOfSentiments(data)

        splitTextData = self.__testTrainSplit(textData)
        splitSentimentData = self.__testTrainSplit(sentimentData)

        trainText = splitTextData[0]
        testText = splitTextData[1]

        trainSentiment = splitSentimentData[0]
        testSentiment = splitSentimentData[1]

        vectText = self.__trainVectoriser(trainText, testText, vectModelPath)
        vectTrain = vectText[0]
        vectTest = vectText[1]

        # Trains the model
        NB.fit(vectTrain, trainSentiment)
        sentiment = NB.predict(vectTest) # Tests the model

        # Save model
        self.__savePickle(modelPath, NB)

        # How accurate the model is
        print("accuracy: {}".format(accuracy_score(testSentiment, sentiment)))

    def predictPolarity(self, data, modelPath, vectModelPath):
        vectData = self.__featureExtraction(data, vectModelPath)
        model = self.__loadPickle(modelPath)
        sentiment = model.predict(vectData)
        return sentiment     
    
    def __trainVectoriser(self, trainText, testText, modelPath):
        vect = TfidfVectorizer()
        vectTrain = vect.fit_transform(trainText)
        vectTest = vect.transform(testText)

        self.__savePickle(modelPath, vect)

        return (vectTrain, vectTest)

    # Gives a numerical value based on how common the word is
    def __featureExtraction(self, text, modelPath):
        vect = self.__loadPickle(modelPath)
        return vect.transform(text)

    def __testTrainSplit(self, data):
        splitData = int(round(len(data) * self.__TRAINPERCENTAGE))

        trainData = data[:splitData]
        testData = data[splitData:]

        return trainData, testData

    # Loads the specified .pickle file
    def __loadPickle(self, file):
        return pickle.load(open(file, 'rb'))

    # Saves data as a .pickle file
    def __savePickle(self, file, obj):
        f = open(file, 'wb')
        pickle.dump(obj, f)
        f.close()