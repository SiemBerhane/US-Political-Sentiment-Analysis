from Backend.Hashing import HashTable
from Backend.TextProcessing import GatherTweetData

# ht = HashTable(15)
# gtd = GatherTweetData(10, 0)
# tt = gtd.testTweets()

# for obj in tt:
#     ht.addItem(obj.key, obj)

# ht.testHashing()

tweetCollecter = GatherTweetData(10, 5)
x = tweetCollecter.getLocation('New York')
print(x, type(x))