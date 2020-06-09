"""
Script #1
Retrieve all the latest tweets of the chosen usernames (see screen_name_list)
Need to create a file called twitter_credentials.py in the same folder. This file will store the keys to log in to the twitter app
"""

import tweepy
import pandas as pd
import simplejson as json
import datetime

import twitter_credentials #Python file which contains only my twitter credentials as global variables

def get_posts(username):
    """
    Function retrieving as much tweets as possible of a specific user
    :param username: The name after the @ in Twitter
    :return: a list of string, where a cell correspond to a tweet
    """

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    alltweets=[]

    new_tweets = api.user_timeline(screen_name = username,count=200,tweet_mode='extended')
    status = new_tweets[0]
    json_str = json.dumps(status._json)

    #convert to string
    json_str = json.dumps(status._json)
    #deserialise string into python object
    parsed = json.loads(json_str)
    print(json.dumps(parsed, indent=4, sort_keys=True))

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=username, count=200, max_id=oldest,tweet_mode='extended')

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(f"...{len(alltweets)} tweets downloaded so far")


    outtweets=[]


    for item in alltweets:

        mined = {
            'tweet_id': item.id,
            'name': item.user.name,
            'screen_name': item.user.screen_name,
            'retweet_count': item.retweet_count,
            'lang' : item.lang,
            'text': item.full_text,
            'mined_at': datetime.datetime.now(),
            'created_at': item.created_at,
            'favourite_count': item.favorite_count,
            'hashtags': item.entities['hashtags'],
            'status_count': item.user.statuses_count,
            'location': item.place,
            'source_device': item.source
        }

        try:
            mined['retweet_text'] = item.retweeted_status.full_text # In case the tweet is a RT, there is a need to
            # retrieve the retweet_text field which contains the full comment (up to 280 char) accompanying the retweet
        except:
            mined['retweet_text'] = ''

        outtweets.extend([mined])

    return outtweets


#We can now call the above function in order to retrive tweets of several users
screen_name_list=["el_pais","elmundoes","abc_es","LaVanguardia","ExpansionMx"]#4 most popular Spanish newspapers, and one newspaper specialised in economics/business

#Init dataframe with first user
screen_name_list_start=screen_name_list[0]
df=pd.DataFrame(get_posts(screen_name_list_start))

#Fill dataframe with all next users
try:
    screen_name_list_end=screen_name_list[1:]

    for current_username in screen_name_list_end:
        current_df = pd.DataFrame(get_posts(current_username))
        # df.append(current_df,ignore_index=True)#does not work=> use concat
        df=pd.concat([df, current_df])
except:
    print("error in username listing")

#Save (csv for ease of reuse, excel for human-readibility)
df.to_csv(r".\1.Tweets\AllTweets.csv")
df.to_excel(r".\1.Tweets\AllTweets.xlsx")