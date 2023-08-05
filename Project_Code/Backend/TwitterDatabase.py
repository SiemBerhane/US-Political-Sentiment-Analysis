# Will hold all the data in different lists based on different factors
class TwitterDataStore:
    # List of twitter data objects
    def __init__(self):
        self.completeList = []
        self.repubTweetsList = []
        self.demTweetsList = []
        self.posList = []
        self.negList = []
