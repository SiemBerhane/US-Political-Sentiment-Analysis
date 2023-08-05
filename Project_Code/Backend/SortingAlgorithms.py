# https://isaaccomputerscience.org/concepts/dsa_search_merge?examBoard=aqa&stage=a_level

class Algorithms:

    def mergeSort(self, items, asc):
    # Base case for recursion:
    # The recursion will stop when the list has been divided into single items
        if len(items) <= 1:
            return items
        else:
            midpoint = (len(items)-1) // 2 # Calculate the midpoint index
            leftHalf = items[0:midpoint+1] # Create left half list
            rightHalf = items[midpoint+1:len(items)] # Create right half list

            leftHalf = self.mergeSort(leftHalf, asc) # Recursive call on left half
            rightHalf = self.mergeSort(rightHalf, asc) # Recursive call on right half
            
            # Call funtion to merge both halves
            if asc:
                mergedItems = self.__mergeAscending(leftHalf, rightHalf) 
            else:
                mergedItems = self.__mergeDescending(leftHalf, rightHalf)

            return mergedItems

    def __mergeAscending(self, left, right):
        merged = [] # New list for merging the items
        indexLeft = 0 
        indexRight = 0 

        # While there are still items to merge
        while indexLeft < len(left) and indexRight < len(right):

            # Find the lowest of the two items being compared 
            if left[indexLeft] < right[indexRight]:
                merged.append(left[indexLeft])
                indexLeft += 1
            else:
                merged.append(right[indexRight])
                indexRight += 1

        # Add to the merged list any remaining data from left list
        while indexLeft < len(left):
            merged.append(left[indexLeft])
            indexLeft += 1

        # Add to the merged list any remaining data from right list
        while indexRight < len(right):
            merged.append(right[indexRight])
            indexRight += 1

        return merged

    # Works the same as ascending
    def __mergeDescending(self, left, right):
        merged = [] 
        indexLeft = 0 
        indexRight = 0 

        while indexLeft < len(left) and indexRight < len(right):

            if left[indexLeft] < right[indexRight]:
                merged.append(right[indexRight])
                indexRight += 1
            else:
                merged.append(left[indexLeft])
                indexLeft += 1

        while indexLeft < len(left):
            merged.append(left[indexLeft])
            indexLeft += 1

        while indexRight < len(right):
            merged.append(right[indexRight])
            indexRight += 1

        return merged    



# x = Algorithms()
# y = x.mergeSort(['a', 'c', 'e', 'v', 'b', 'y', 'e'], asc=True)
# print(y)