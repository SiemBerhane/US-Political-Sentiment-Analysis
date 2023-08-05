class TwitterData():
    def __init__(self, text, cleanText=None, sentiment=None, loc=None, creationDate=None, username=None, 
    lang=None, key=None, tweetMetrics=None, republican=None, userMetrics=None):
        self.text = text
        self.cleanText = cleanText
        self.sentiment = self.__getSentiment(sentiment)
        self.location = loc
        self.username = username
        self.lang = lang
        self.repub = self.__getRepub(republican)
        self.metrics = tweetMetrics # Dictionary of metrics such as likes, retweets etc.
        self.userMetrics = self.__metricsDict(userMetrics)
        self.key = key # Will be used as the hashing key

        self.__setDate(creationDate)


    # Returns true if the tweet mentions the Republicans
    def __getRepub(self, repub):
        isRepub = True
        if repub == 'TRUE':
            isRepub = True
        else:
            isRepub = False
        
        return isRepub

    # Gets rid of the unnecessary characters found in the sentiment column in the .csv file
    def __getSentiment(self, sent):
        newSent = sent.replace("[", "")
        newSent = newSent.replace("]", "")
        newSent = newSent.replace("'", "")
        return newSent

    # Converts the metrics column from a string to a dictionary
    def __metricsDict(self, metrics):
        lst = []
        metrics = metrics.split(" ")
        for part in metrics:
            newPart = part.replace("{", "")
            newPart = newPart.replace("}", "")
            newPart = newPart.replace(",", "")
            newPart = newPart.replace(":", "")
            newPart = newPart.replace("'", "")
            lst.append(newPart)

        metricsDict = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return metricsDict

    # Gets the time and date
    def __setDate(self, timeData):
        date = timeData[0:10]
        time = timeData[11:19]

        return (time, date)
        
        
