from Backend.LinkedList import Node, LinkedList

class HashTable:
    def __init__(self, len):
        self.table = [None] * len
        self.len = len

    # The last 5 digits of id will be key, the twitterObj will be obj
    def addItem(self, key, obj):
        twitterObj = Node(obj)
        index = self.__hashingAlgorithm(key)
        
        if self.table[index] != None: # If there is already an object at that point
            self.__addToLinkedList(twitterObj, self.table[index]) # Add to the objects linked list
        else:
            self.table[index] = self.__createLinkedList(twitterObj)

    # Returns the item with the specified key
    def getItem(self, key):
        node = None
        index = self.__hashingAlgorithm(key)
        lList = self.table[index]

        # Looks for the node in the linked list
        if lList.head.data.key != key: 
            node = lList.findNode(key) # The node was not the head of the list
        else: 
            node = lList.head # The node was the head of the list

        return node.data

    def __createLinkedList(self, node):
        lList = LinkedList(node)
        return lList

    # Adds node to the end of a linked list
    def __addToLinkedList(self, node, lList):
        lastNode = lList.getLastNode()
        lastNode.next = node

    def __hashingAlgorithm(self, key):
        return key % self.len

    def traverseListTest(self, index):
        lList = self.table[index]
        lList.traverseListTest()

    # Used to test if the algorith works
    def testHashing(self):
        for llist in self.table:
            if llist == None:
                continue

            lastNode = llist.getLastNode()

            if lastNode.data.id != llist.head.data.id:
                llist.traverseListTest()
                continue

            print(f"This is the only item stored {llist.head.data.id}")





