import tweepy
import time
import mySecrets

consumer_key = mySecrets.secrets['consumer_key']
consumer_secret = mySecrets.secrets['consumer_secret']
key = mySecrets.secrets['key']
secret = mySecrets.secrets['secret']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)
file_name = 'last_tweet'

# holds the last tweet id
def last_tweet(file_name):
    read = open(file_name, 'r')
    read_id = int(read.read().strip())
    read.close()
    return read_id

# replaces the new tweet id with a new tweet id
def new_tweet(file_name, read_id):
    new_id = open(file_name, 'w')
    new_id.write(str(read_id))
    new_id.close()
    return


tweets = api.mentions_timeline(last_tweet(file_name), tweet_mode='extended')


# this will communicate with users once 'jeffiscode' is tagged
def auto():
    for tweet in tweets:
        if '@jeffiscode' in tweet.full_text.lower():
            print('tweet from ' + tweet.user.name + str(tweet.id) + ' - ' + tweet.full_text)
            api.update_status('@' + tweet.user.screen_name + ' Yes, I am here!', tweet.id)
            api.retweet(tweet.id)
            api.create_favorite(tweet.id)
            new_tweet(file_name, tweet.id)

# searches through hashtags and users
# it will like and retweet a given amount of posts
def search(result, amount):
    searches = tweepy.Cursor(api.search, result).items(amount)

    for search in searches:
        try:
            search.retweet()
            search.favorite()
            print("Post retweeted and liked")
            time.sleep(2)
        except tweepy.TweepError as a:
            print(a.reason)
            time.sleep(2)

# follows all users who are following you but you're not following back
def follow_users():
    followers = tweepy.Cursor(api.followers).items()

    for follower in followers:
        if not follower.following:
            try:
                follower.follow()
                print('Now following ' + follower.name)
            except tweepy.TweepError as b:
                print(b.reason)

# unfollows users who you're following but they're not following back
def unfollow_users():
    followerS = tweepy.Cursor(api.followers).items()
    friends = tweepy.Cursor(api.friends).items()

    for unfollower in friends:
        if unfollower not in followerS:
            ask = input('would you like to unfollow ' + unfollower.name + ' (y/n)? ')
            if ask == 'y':
                print('This user: ' + unfollower.name + ' has unfollowed you, we did the same')
                unfollower.unfollow()
                time.sleep(3)

# follows an individual user
def follow(user):
    try:
        api.create_friendship(user)
        print('Friend request sent to ' + user)
        time.sleep(5)
    except tweepy.TweepError as b:
        print(b.reason)
        time.sleep(2)

# unfollow an individual user
def unfollow(user):
    try:
        api.destroy_friendship(user)
        print("Succesfully unfollowed " + user)
        time.sleep(5)
    except tweepy.TweepError as c:
        print(c.reason)
        time.sleep(2)


if __name__ == '__main__':
    # auto()
    # search()
    # follow_users()
    # unfollow_users()
    # follow('yodemik')
    # unfollow()