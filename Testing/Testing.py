from curses import newpad
import re 
from tkinter import Y
from xml.etree.ElementTree import tostring
import pandas as pd
from geopy.geocoders import Nominatim
from enum import Enum

# location = Nominatim(user_agent="Hello").geocode('fhjksdhf', addressdetails=True)


# try: 
#     #print(location.address.split(',')[-1])  
#     address = location.raw['address']
#     state = address['state']
#     print(address, state)
#     # listAddress = address.split(',')
#     # print(listAddress)
# except KeyError:
#     print(":(")

# except:
#     print(":((")


# x = {1:'a', 2:'b', 3:'c'}
# y = x.keys()
# for z in y:
#     print(z)

# nlp = spacy.load("en_core_web_sm")
# x = "yep torturing care"
# docs = nlp(x)
# newDoc = ""
# for token in docs:
#     newDoc += token.lemma_ + ' '

# x = 'followers_count'
# y = "{'followers_count': 3, 'following_count': 175, 'tweet_count': 165, 'listed_count': 0}".split(" ")
# z = []
# x = "['x']"
# y = x.replace("[", "")
# y = y.replace("]", "")
# y = y.replace("'", "")
# print(y)

x = {
    'a':1,
    'b':2,
    'c':3
}

for item in x:
    print(item, x[item])
