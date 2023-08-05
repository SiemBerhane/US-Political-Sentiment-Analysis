from Frontend.Layouts import LayoutHandler

from enum import Enum
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QGridLayout, 
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QButtonGroup,
    QStackedWidget)


class MainWindow(QMainWindow):
    def __init__(self, tweets, mainClass, cList, calcData):
        super().__init__()
        self.main = mainClass # Instance of the main class
        self.calcData = calcData # Instance of the CalculateTweetData class
        self.currentList = cList # The current list displayed
        self.boldFont = QFont()
        self.boldFont.setBold(True)
        self.__initialiseMenu()
        self.__initScreen(tweets)

    # Initialises the screen
    def __initScreen(self, tweets):
        self.buttons = QButtonGroup() # Group of buttons that have a unique ID
        self.widgetDict = {}
        self.stackWidget = QStackedWidget() # List of pre made widgets
        tweetsWidget = QWidget(self)
        tweetLayout = QVBoxLayout(self)

        # Displays the username and tweet as a single object that can be interacted with via button (username)
        # The username is displayed as a button and the tweet is stored as a label
        for tweet in tweets:
            # The username and tweet are added to a vertical layout which is then added to another vertical layout
            tweetContainer = QWidget(tweetsWidget)
            tweetContainerLayout = QVBoxLayout(tweetsWidget)
            
            username = QPushButton(tweetsWidget, text=tweet.username)
            username.setFont(self.boldFont) # The username will be bold to help make it stand out
            tweetLabel = QLabel(tweetsWidget, text=tweet.text)
            tweetLabel.setWordWrap(True) # Text moves on to a new line if it's too big

            # Add the username and text to the same layout
            tweetContainerLayout.addWidget(username)
            tweetContainerLayout.addWidget(tweetLabel)

            # Add the button to the button group, the tweet key will be the button ID
            # This makes it easy to retrieve the tweet data from the hash table
            self.buttons.addButton(username, tweet.key)
        
            # Add it to the main tweet layout
            tweetContainer.setLayout(tweetContainerLayout)
            tweetLayout.addWidget(tweetContainer)

        # Return the ID of the button clicked
        self.buttons.idClicked.connect(self.__usernamePressed)
        tweetsWidget.setLayout(tweetLayout)

        # Able to scroll through the tweets 
        scroll = QScrollArea(self)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(tweetsWidget)

        # Will contain the data to do with the tweet/tweets
        self.rightWidget = QWidget(self)
        self.rightWidget.setLayout(self.__rightLabelText())        
        self.widgetDict[0] = self.stackWidget.addWidget(self.rightWidget)
        self.stackWidget.setCurrentIndex(self.widgetDict[0])

        # Able to scroll through the data
        rightScroll = QScrollArea(self)
        rightScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        rightScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        rightScroll.setWidgetResizable(True)
        rightScroll.setWidget(self.stackWidget)

        # The left side are the tweets & the right side is the data 
        self.gridLayout = QGridLayout(self)

        self.gridLayout.addWidget(scroll, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addWidget(rightScroll, 1, 1, 1, 2)

        gridWidget = QWidget(self)
        gridWidget.setLayout(self.gridLayout)

        self.setCentralWidget(gridWidget)

    # Displays the specific data if a button is pressed
    def __usernamePressed(self, buttonID):
        # Get the data from the hash table using the buttonID as the key
        tweetData = self.main.getItemFromHash(buttonID) 
        vertLayout = QVBoxLayout()
        vertLayoutWidget = QWidget()

        # Makes the data appear more readable to the user
        if tweetData.repub:
            party = 'Republican'
        else:
            party = 'Democrat'

        if len(tweetData.location) == 0:
            tweetData.location = 'Not Available'

        dataDict = {'Username: ': tweetData.username,
        'Sentiment: ': tweetData.sentiment,
        'Location: ': tweetData.location,
        'Party: ': party}

        # Loops through the data so it can be displayed
        for item in dataDict:
            horLayoutWidget = QWidget()
            horLayout = QHBoxLayout()

            title = QLabel(text=item)
            data = QLabel(text=dataDict[item])

            # Adds the data to a horizontal layout
            horLayout.addWidget(title)
            horLayout.addWidget(data)
            horLayoutWidget.setLayout(horLayout)
            vertLayout.addWidget(horLayoutWidget)
            

        # Loops through all the metrics dictionary and adds them to display
        for metric in tweetData.userMetrics:
            horLayoutWidget = QWidget()
            horLayout = QHBoxLayout()

            # Makes the data more presentable to the user
            if metric == 'followers_count':
                titleText = 'Number of Followers: '
            elif metric == 'following_count':
                titleText = 'Number of Accounts Following: '
            elif metric == 'tweet_count':
                titleText = 'Number of Tweets: '
            else:
                titleText = 'Number of Lists Added to: '

            title = QLabel(text=titleText)
            data = QLabel(text=tweetData.userMetrics[metric])

            # Adds to a horizontal layout
            horLayout.addWidget(title)
            horLayout.addWidget(data)
            horLayoutWidget.setLayout(horLayout)
            vertLayout.addWidget(horLayoutWidget)

        vertLayoutWidget.setLayout(vertLayout)

        self.widgetDict[buttonID] = self.stackWidget.addWidget(vertLayoutWidget)
        self.__updateRightLabel(buttonID)        

    # Displays the general data
    def __rightLabelText(self):
        cList = self.main.getCurrentList()
        dataDict = self.calcData.generalData(cList) # Gets the general data
        vertLayout = QVBoxLayout()

        for item in dataDict:
            horWidget = QWidget()
            horLayout = QHBoxLayout()
            title = QLabel(text=item)

            # If the data in the dictionary isn't a string, convert it to one
            if not isinstance(dataDict[item], str):
                data = QLabel(text=str(dataDict[item]))
            else:
                data = QLabel(text=dataDict[item])

            # Adds to horizontal layouy
            horLayout.addWidget(title)
            horLayout.addWidget(data)
            horWidget.setLayout(horLayout)
            vertLayout.addWidget(horWidget)        
        
        return vertLayout
    
    # Changes the data displayed based on what has been selected
    def __updateRightLabel(self, key):
        self.stackWidget.setCurrentIndex(self.widgetDict[key])

    # Initialises the main bar at the top of the window
    def __initialiseMenu(self):
        filterComboList = ['Filters', 'Republicans', 'Democrats', 'Positive', 'Negative']
        userComboList = ['Sort', 'Most Followers', 'Least Followers', 'A-Z', 'Z-A']

        # Creates drop down boxes
        self.filterCombo = self.__addComboBox(filterComboList)
        self.userCombo = self.__addComboBox(userComboList)

        # Resets the window
        refreshButton = QPushButton(parent=self, text='Refresh')

        # Calls these functions when one of the options is pressed
        self.filterCombo.activated.connect(self.__updateFilterState)
        self.userCombo.activated.connect(self.__updateUserState)
        refreshButton.clicked.connect(self.__resetLabels)

        # Pins them to the top of the window
        menuWidget = QWidget()
        menuWidgetsList = [self.filterCombo, self.userCombo, refreshButton]
        menuLayout = LayoutHandler.createHBox(parent=self, widgets=menuWidgetsList)
        menuWidget.setLayout(menuLayout)
        self.setMenuWidget(menuWidget)

    # Resets the window
    def __resetLabels(self):
        self.main.refreshDisplay()

    # The index of the button corresponds to which button was pressed
    def __updateFilterState(self, index):
        self.main.filterTweets(index)
        
    # The index of the button corresponds to which button was pressed
    def __updateUserState(self, index):
        if index == 1: # Most followers
            self.main.orderByFollowerCount(False)
        elif index == 2: # Least followers
            self.main.orderByFollowerCount(True)
        elif index == 3: # A-Z
            self.main.orderByUsername(True)
        elif index == 4: # Z-A
            self.main.orderByUsername(False)

    def __addComboBox(self, text):
        cBox = QComboBox(self)
        cBox.addItems(text)
        return cBox

# Enums
class FilterComboState(Enum):
    COMPLETE = 0
    REPUB = 1
    DEM = 2
    POS = 3
    NEG = 4

class TweetComboState(Enum):
    SORT_TWEETS = 0
    MOST_LIKES = 1
    LEAST_LIKES = 2

class UserComboState(Enum):
    SORT_USERS = 0
    MOST_FOLLOWERS = 1
    LEAST_FOLLOWERS = 2

class LayoutType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    GRID = 2

