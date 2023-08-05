import sys
from enum import Enum
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget,
    QLabel,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout, 
    QPushButton,
    QMainWindow,
    QMessageBox,
    QScrollArea)

# https://www.youtube.com/watch?v=vIqw411xoj0 - display box
# https://www.pythonguis.com/tutorials/pyqt6-qscrollarea/ - scrolling
# https://stackoverflow.com/questions/9378894/how-to-add-a-fixed-header-to-a-qscrollarea - possible solution to 
# adding scroll area to a specific part of the grid 

class LayoutType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    GRID = 2

class FilterComboState(Enum):
    FILTERS = 0
    REUPLICANS = 1
    DEMOCRATS = 2
    POSITIVE = 3
    NEGATIVE = 4

class TweetComboState(Enum):
    SORT_TWEETS = 0
    MOST_LIKES = 1
    LEAST_LIKES = 2

class UserComboState(Enum):
    SORT_USERS = 0
    MOST_FOLLOWERS = 1
    LEAST_FOLLOWERS = 2

class LabelHandler:
    def __init__(self):
        self.listOfLabels = [] # Will be a queue
        self.back = 0

    def createLabels(self, parent, num):
        tempList = []
        for i in range(num):
            label = QLabel(parent=parent)
            tempList.append(label)
            self.__storeLabel(label)

        tempList = self.initialiseLabels(tempList)
        return tempList

    def __storeLabel(self, label):
        self.listOfLabels.append(label)

    def __removeLabel(self):
        self.listOfLabels.pop(0) # Removes the first element of the list

    def initialiseLabels(self, labelList): # When the filters havent been changed
        for label in labelList:
            label.setText("hello \n hi")

        return labelList

    def __updateLabels(self, text):
        for label in self.listOfLabels:
                #self.__removeLabel()
                label.setText(text)
                #self.__storeLabel(label)

    def filterLabels(self, fState):
        # Repeat for rest of states - could probably condense into seperate functions
        if fState is FilterComboState.FILTERS:
            self.__updateLabels('YO')
        elif fState is FilterComboState.DEMOCRATS:
            self.__updateLabels('HEY')
        elif fState is FilterComboState.REUPLICANS:
            self.__updateLabels('BYE')
        elif fState is FilterComboState.POSITIVE:
            self.__updateLabels('NO')
        else:
            self.__updateLabels('YES')

    def tweetLabels(self, tState):
        if tState is TweetComboState.SORT_TWEETS:
            self.__updateLabels('BON')
        elif tState is TweetComboState.MOST_LIKES:
            self.__updateLabels('NON')
        else:
            self.__updateLabels('OUI')

    def userLabels(self, uState):
        if uState is UserComboState.SORT_USERS:
            self.__updateLabels(':(')
        elif uState is UserComboState.MOST_FOLLOWERS:
            self.__updateLabels(':(')
        else:
            self.__updateLabels(':|')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.labelHandler = LabelHandler()
        self.boldFont = QFont()
        self.boldFont.setBold(True)
        self.__initialiseScreen()
        self.initialiseMenu()

    def __initialiseScreen(self):
        self.setWindowTitle('Test :)')

        # Left side vertical labels
        #leftLabels = self.labelHandler.createLabels(self, 50)
        #labelLeftWidget = self.CreateLayout(LayoutType.VERTICAL, leftLabels, False, 0, 0)

        # Creates a VLayout which contains username(QPushbutton) & the tweet(QLabel)
        # Adds it to another VLayout
        tweetsWidget = QWidget(self)
        tweetLayout = QVBoxLayout(self)

        for i in range(4):
            tweetContainer = QWidget(tweetsWidget)
            tweetContainerLayout = QVBoxLayout(tweetsWidget)
            
            username = QPushButton(tweetsWidget, text='HI')
            username.setFont(self.boldFont)
            tweet = QLabel(tweetsWidget, text='jfklsjf')

            tweetContainerLayout.addWidget(username)
            tweetContainerLayout.addWidget(tweet)
            tweetContainer.setLayout(tweetContainerLayout)
            tweetLayout.addWidget(tweetContainer)

        tweetsWidget.setLayout(tweetLayout)


        # Rigth side vertical labels
        rightLabels = self.labelHandler.createLabels(self, 3)
        labelRightWidget = self.CreateLayout(LayoutType.VERTICAL, rightLabels, False, 0, 0)

        scroll = QScrollArea(self)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(tweetsWidget)

        # Grid layout where the left side occupies 1/3 of the space and the 
        # Rest is filled out by right side widgets
        gridLayout = QGridLayout(self)

        gridLayout.addWidget(scroll, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        gridLayout.addWidget(labelRightWidget, 1, 1, 1, 2)

        gridWidget = QWidget(self)
        gridWidget.setLayout(gridLayout)
        # mainWidget = self.CreateLayout(LayoutType.HORIZONTAL, gridw, False, 1, 1)

        self.setCentralWidget(gridWidget)


    def initialiseMenu(self):
        filterComboList = ['Filters', 'Republicans', 'Democrats', 'Positive', 'Negative']
        tweetComboList = ['Sort Tweets', 'Most Likes', 'Least Likes']
        userComboList = ['Sort Users', 'Most Followers', 'Least Followers']

        self.filterCombo = self.__AddComboBox(filterComboList)
        self.tweetCombo = self.__AddComboBox(tweetComboList)
        self.userCombo = self.__AddComboBox(userComboList)

        refreshButton = QPushButton(parent=self, text='Refresh\nHi')
        #refreshButton.setFont(boldFont)

        self.filterCombo.activated.connect(self.updateFilterState)
        self.tweetCombo.activated.connect(self.updateTweetState)
        self.userCombo.activated.connect(self.updateUserState)
        refreshButton.clicked.connect(self.resetLabels)

        menuWidgetsList = [self.filterCombo, self.tweetCombo, self.userCombo, refreshButton]
        
        menuWidget = self.CreateLayout(LayoutType.HORIZONTAL, menuWidgetsList, False, 0, 0)
        self.setMenuWidget(menuWidget)

    
   
    def updateFilterState(self, index):
        filterState = FilterComboState(index)
        self.labelHandler.filterLabels(filterState)
        
    def updateTweetState(self, index):
        tweetState = TweetComboState(index)
        self.labelHandler.tweetLabels(tweetState)

    def updateUserState(self, index):
        userState = UserComboState(index)
        self.labelHandler.userLabels(userState)

    def resetLabels(self):
        self.labelHandler.initialiseLabels(self.labelHandler.listOfLabels)
        self.resetComboBoxes()
        
    def resetComboBoxes(self):
        self.filterCombo.setCurrentIndex(0)
        self.tweetCombo.setCurrentIndex(0)
        self.userCombo.setCurrentIndex(0)


    def scrollProperties(self, scroll):
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        return scroll

    # Return widget
    def CreateLayout(self, layoutType, widgets, isStrech, strIndex, strFactor):
        try:
            hostWidget = QWidget(self)
            if layoutType is LayoutType.HORIZONTAL:
                layout = LayoutHandler.createHBox(self, widgets, isStrech, strIndex, strFactor)
            elif layoutType is LayoutType.VERTICAL:
                layout = LayoutHandler.createVBox(self, widgets)
            elif layoutType is LayoutType.GRID:
                layout = LayoutHandler.createGrid(self, widgets)
        
        except AttributeError: # If layoutType is invalid
            print("layoutType might be invalid")
            # Throw an error, could have a seperate class/function that handles it all
        
        hostWidget.setLayout(layout)
        return hostWidget

    def __AddComboBox(self, text):
        cBox = QComboBox(self)
        cBox.addItems(text)
        return cBox

    def DialogueBox(self, title):
        newWindow = QMessageBox(self)
        newWindow.setWindowTitle(title)
        newWindow.setText('cock :)')
        newWindow.exec() # Stops interactions to any other windows


class LayoutHandler:
    def createHBox(parent, widgets, isStretch, index, stretch):
        horLayout = QHBoxLayout(parent)
        c = 1

        for w in widgets:
            if c == 0:
                horLayout.addWidget(w, alignment=Qt.AlignmentFlag.AlignLeft)
            else:
                horLayout.addWidget(w)
            c+= 1

        if isStretch:
            horLayout.insertStretch(index, stretch)
        
        return horLayout

    def createVBox(parent, widgets):
        vertLayout = QVBoxLayout(parent)

        for w in widgets:
            vertLayout.addWidget(w)
        
        return vertLayout

    def createGrid(parent, widgets, r, c, rSpan, cSpan):
        gridLayout = QGridLayout(parent)

        for w in widgets:
            gridLayout.addWidget(w, r, c, rSpan, cSpan)
        
        return gridLayout


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec()) # Starts the event loop
