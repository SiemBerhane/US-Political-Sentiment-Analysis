# Class of the obj which will hold data + pointer to next obj
class Node:
    def __init__(self, d):
        self.data = d
        self.next = None

class LinkedList:
    def __init__(self, h):
        self.head = h
        self.lastNode = h.next

    # Finds the node at the end of the list
    def getLastNode(self):
        endOfList = False
        temp = self.head

        while not endOfList:
            if temp.next == None:
                endOfList = True
            else:
                temp = temp.next

        return temp

    # Finds the node with the specified ID
    def findNode(self, id):
        temp = self.head
        nodeFound = False
        
        while not nodeFound:
            if temp.data.key != id:
                temp = temp.next
            else:
                nodeFound = True
        
        return temp



    