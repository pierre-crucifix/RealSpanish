"""
Script #2
Clean all tweet texts
    Are removed :
        * tweets with a language label other than Spanish
        * emojis
        * all punctuation marks
        * all numbers
        * all urls
        * all #hashtag_text
        * all @twitter_username_mention
        * capital letters are reduced
        * tweets text longer than 141-280 characters in context of RT are fixed
"""

import pandas as pd
import string
import re
import emoji

df=pd.read_csv(r".\1.Tweets\AllTweets.csv")
# df=df.head(100)#A retirer à la fin

#Remove tweets with other language than Spanish
lang_mask=df["lang"]=="es"
df=df[lang_mask]

#Cast to string
df_tweets=df.copy()[["text","retweet_text"]]
df_tweets=df_tweets.astype(str)

#In case of RT, tweet text is cropped at 140 car, so it has to be replaced by retweet_text (which is the text of the person who retweet) and which is complete
mask=df_tweets["retweet_text"]!="nan"
df_tweets["text"][mask]=df_tweets["retweet_text"]
df_tweets=df_tweets.drop(columns=["retweet_text"])


# sample_string_split=nltk.word_tokenize(sample_string)
# print(sample_string_split)

# sample_string = re.sub(r"^\d+\s|\s\d+\s|\s\d*$", "", sample_string)
# # sample_string = re.sub(r"^[^\P{P}-]+", "", sample_string)
# sample_string = sample_string.lower()


def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

#Add the reverse question mark (typically Spanish) to the list of punctuation string
string.punctuation=string.punctuation+"¿"
#Add “ and ” and ‘ and ’ and — and « and » and other ones
string.punctuation=string.punctuation+"“"+"”"+"‘"+"’"+"—"+"«"+"»"

print("All ponctuation marks that are going to be discarded : "+string.punctuation)
def clean_text(text):
    """
    Function cleaning a sentence given as a string
    :param text: sentence as a string
    :return: a string with all the words constituting the sentence
    """
    text=remove_emoji(text) #remove emoji #https://stackoverflow.com/questions/51784964/remove-emojis-from-multilingual-unicode-text

    text = ''.join([i for i in text if not i.isdigit()]) #removing numbers

    nopunc = [char for char in text if char not in string.punctuation] # Check characters to see if they are in punctuation

    nopunc = ''.join(nopunc) # Join the characters again to form the string.

    nopunc = nopunc.lower() # convert text to lower-case

    # remove URLs
    nopunc = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', nopunc)
    nopunc = re.sub(r'http\S+', '', nopunc)

    nopunc = re.sub('@[^\s]+', '', nopunc)# remove usernames
    # # remove the # in #hashtag
    # nopunc = re.sub(r'#([^\s]+)', r'\1', nopunc)
    # remove words that are #hashtag
    nopunc = re.sub(r'#([^\s]+)', '', nopunc)
    # # remove repeated characters
    # nopunc = word_tokenize(nopunc)
    # # remove stopwords from final word list
    # text= [word for word in nopunc if word not in stopwords.words('english')]
    return nopunc


### Clean tweets
df_tweets["text"]=df_tweets["text"].apply(lambda x : clean_text(x))
#Note the above line can take profit of parallel computing if needed (for larger db)
#See https://towardsdatascience.com/pandaral-lel-a-simple-and-efficient-tool-to-parallelize-your-pandas-operations-on-all-your-cpus-bb5ff2a409ae

df_tweets.to_csv(r".\2.Cleaned Tweets\CleanedTweets.csv")
df_tweets.to_excel(r".\2.Cleaned Tweets\CleanedTweets.xlsx")