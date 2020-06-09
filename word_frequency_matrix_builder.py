"""
Script #3
1)  Build a dataframe of two columns: the first one contains unique words, the second one their frequency
    NOTE THAT stopwords are removed (we consider a learner having already passed a lesson about stopwords)
2)  Create a new column to cleaned_tweets dataframe where each cell includes in a list all the words (string) present in the tweet of the same row
3)  [Still in development-phase] Manage an automated translation thanks to googletrans (still in implementation)
"""

import pandas as pd
import nltk
nltk.download('stopwords') #To uncomment at the first use, and to comment later on
from nltk.corpus import stopwords
from googletrans import Translator

df_tweets=pd.read_csv(r".\2.Cleaned Tweets\CleanedTweets.csv",index_col=0)
# df_tweets=df_tweets.head(100)#A retirer à la fin

def remove_stopwords(text):
    """
    Remove stopwords of a given sentence
    :param text: a sentence in string type
    :return: the same sentence, still in string type, but without stopwords
    """
    text_split=text.split()
    text_split=[word for word in text_split if word not in stopwords.words('spanish')]
    return text_split


### Split 1 string per tweet to 1 array of words for each tweet ; Also remove the stopwords at the same time
df_tweets["words"]=df_tweets["text"].apply(lambda x : remove_stopwords(x))

df_tweets.to_csv(r".\3.Word Matrices\CleanedTweets.csv")
df_tweets.to_excel(r".\3.Word Matrices\CleanedTweets.xlsx")

### Managing the frequency of each word
words_list=[]

for index, value in df_tweets["words"].iteritems():#It is a series not a dataframe => iteritems instead of iterrows
    for word in value:
        words_list.append(word)

df_words=pd.DataFrame(words_list, columns=["words"])
series_word_frequency_counter=df_words["words"].value_counts()
print(series_word_frequency_counter)

df_word_frequency_counter=series_word_frequency_counter.to_frame()
df_word_frequency_counter.rename(columns={"words":"frequency"},inplace=True)


df_word_frequency_counter["translation"]="blabla"#Ideally to replace by the translation ; note the translation can also be done manually for learning purpose but also to ensure a better accuracy

#Trying to translate with Google Translate, but did not work - apparently due to a refusal on server side - to be re-tried later

# df_word_frequency_counter=df_word_frequency_counter.head(5)#A retirer à la fin
#
# translator = Translator()
# translator.translate("la mujer", src='es', dest='fr').text
# # print(translator.translate("Test"))
#
# # def translate_word(word):
# #     return translator.translate(str(word), src='es', dest='fr')
# #
# #
# # for index, value in df_word_frequency_counter["translation"].iteritems():#It is a series not a dataframe => iteritems instead of iterrows
# #     string_index = str(index)
# #     df_word_frequency_counter.at[index,"translation"]= translate_word("una").text
# #     # value = translator.translate(string_index, src='es', dest='fr')



df_word_frequency_counter.to_csv(r".\3.Word Matrices\WordsFrequency.csv")
df_word_frequency_counter.to_excel(r".\3.Word Matrices\WordsFrequency.xlsx")