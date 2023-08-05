import tweepy

# https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9
# https://www.sahilfruitwala.com/guide-to-extract-tweets-using-tweepy

client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAPORgQEAAAAA7ZcWW75MRdpMYlZPDh6IHKlzQ1w%3DQBM7812mKRQVghVoJSjvk50aVIrewDLQHqdICx41WI8Si8ChLL")

tweetData = []
#Query = 'from:yacobg42 -is:retweet'
REPUBLICAN_QUERY = "(republican OR republicans) lang:en -democrat -is:retweet"
DEMOCRAT_QUERY = "democrat - republican -is:retweet"

#tweets = api.search_tweets(KEYWORDS, tweet_mode="extended", count=50, lang="en")
repubTweets = client.search_recent_tweets(query=REPUBLICAN_QUERY, tweet_fields=['created_at', 'text', 'id', 'public_metrics'],
expansions='author_id', user_fields=['name', 'username', 'location', 'url'], max_results=10)

# for user in repubTweets.includes['users']:
#     x = user
#     print(x['location'])

for tweet in repubTweets.data:
    tweetID = str(tweet['id'])
    userID = tweet['author_id']
    x = tweet['public_metrics']
    user = client.get_user(id=userID)
    userData = user.data
    username = userData['username']
    loc = userData['location']
    url = "https://twitter.com/twitter/statuses/" + tweetID
    twitterTuple = (url, username)
    tweetData.append(twitterTuple)

print(*tweetData, sep="\n")