from enum import Enum
import sys
from Backend.TextProcessing import GatherTweetData
from Backend.TwitterDatabase import TwitterDataStore
from Backend.Hashing import HashTable
from Backend.SortingAlgorithms import Algorithms

from Frontend.Display import MainWindow
from Frontend.CalculateTweetData import CalculateTweetData

from PyQt6.QtWidgets import QApplication

class CurrentList(Enum):
    COMPLETE = 0
    REPUB = 1
    DEM = 2
    POS = 3
    NEG = 4

class MainClass:
    def __init__(self):
        # Starts the event loop, needed to display the window
        self.app = QApplication(sys.argv)

        # Initalising all the classes 
        self.sorting = Algorithms()
        self.tds = TwitterDataStore()
        self.gtd = GatherTweetData(10)
        self.tweetData = CalculateTweetData(self.sorting)
        self.currentList = CurrentList.COMPLETE
        self.__searchTweets()
        self.hashTable = HashTable(len(self.tds.completeList) * 2) # Create the hash table
        self.__hash(self.tds.completeList) # Add tweets to hash table
        self.__displayTweets(tweetsList=self.tds.completeList) 

        sys.exit(self.app.exec()) # Allows the user to close the program

    # Gets tweets from .csv file and adds them to relevant lists
    def __searchTweets(self):
        tweets = self.gtd.csvToListOfData() 

        for object in tweets:
            self.__storeData(object)

    # Creates a window and displays all the data
    def __displayTweets(self, tweetsList=None):
        self.window = MainWindow(tweetsList, self, self.currentList, self.tweetData)
        self.window.show()

    # Add item to hash table
    def __hash(self, list):
        for item in list:
            self.hashTable.addItem(item.key, item)

    # Gets item from hash table
    def getItemFromHash(self, key):
        return self.hashTable.getItem(key)

    # Displays the list of tweets selected from the drop down box
    def filterTweets(self, index):
        self.currentList = CurrentList(index)
        currentList = self.getCurrentList()
        self.window.close() # Closes the window so a new one can be created
        self.__displayTweets(currentList)

    # Sorts the tweets in alphabetical order of their usernames
    def orderByUsername(self, asc):
        tweetsList = self.getCurrentList()
        tweetDict = {}

        # Adds tweets to a dictionary with their key so they can be easily accessed
        for tweet in tweetsList:
            tweetDict[tweet.username.upper()] = tweet.key

        sortedList = self.__sortItems(tweetDict, asc)
        
        self.window.close()
        self.__displayTweets(sortedList)

    # Same as orderByUsername
    def orderByFollowerCount(self, asc):
        tweetsList = self.getCurrentList()
        tweetDict = {}

        for tweet in tweetsList:
            # Creates dictionary with the follower count as the key and the hash key as the value
            # Allows easy access to the key
            tweetDict[int(tweet.userMetrics['followers_count'])] = tweet.key
        
        sortedList = self.__sortItems(tweetDict, asc)
        
        self.window.close()
        self.__displayTweets(sortedList)

    # Uses the merge sort algorithm to sort the tweets
    def __sortItems(self, dict, asc):
        tempSortedList = []
        sortedTweets = []

        # Creates a list of all the keys in the dictionary and sorts them
        tempSortedList = self.sorting.mergeSort(list(dict.keys()), asc)

        for tweet in tempSortedList:
            sortedTweets.append(self.getItemFromHash(dict[tweet]))
        
        return sortedTweets

    # Gets the list of tweets that's currently displayed
    def getCurrentList(self):
        cList = []

        if self.currentList == CurrentList.COMPLETE:
            clist = self.tds.completeList
        elif self.currentList == CurrentList.REPUB:
            clist = self.tds.repubTweetsList
        elif self.currentList == CurrentList.DEM:
            clist = self.tds.demTweetsList
        elif self.currentList == CurrentList.POS:
            clist = self.tds.posList
        else:
            clist = self.tds.negList

        return clist

    # Resets the window
    def refreshDisplay(self):
        self.__displayTweets(self.tds.completeList)

    # Adds tweets to relevant lists
    def __storeData(self, obj):
        self.tds.completeList.append(obj)

        if obj.repub:
            self.tds.repubTweetsList.append(obj)
        else:
            self.tds.demTweetsList.append(obj)

        if obj.sentiment == 'positive': 
            self.tds.posList.append(obj)
        else:
            self.tds.negList.append(obj)

x = MainClass() # Calls the program



