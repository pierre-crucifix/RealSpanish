"""
Script #4
1)  Create the adjacency matrix of words in tweets.
2)  Two words are considered adjacent iff they are present in the same tweet, which proxy the fact they are used in the same context
    In my situation, I chose not to work with a sparse matrix because my graph is quite dense, but it can be interesting to proceed diffently in another context
3)  Still in my situation, I decided to remove all words with less than 11 occurrences in order to remove the vast majority of mispelled words
"""

import pandas as pd
import numpy as np
from ast import literal_eval
import time

start = time.time()

df_tweets=pd.read_csv(r".\3.Word Matrices\CleanedTweets.csv",index_col=0)
df_words=pd.read_csv(r".\3.Word Matrices\WordsFrequency.csv",index_col=0)

#remove less common words in order to make a more relevant analysis
length_df_words_before_drop=df_words["frequency"].count()
df_words=df_words[df_words["frequency"]>10]#Remove 'uncommon' words because they may be mispelled words, and we have enough words in total for our purpose
length_df_words_after_drop=df_words["frequency"].count()
diff_length=length_df_words_before_drop-length_df_words_after_drop
print("Removed "+str(diff_length)+" ("+str(int(diff_length/length_df_words_before_drop*100)) +"%) words with a low frequency")

df_tweets["words"] = df_tweets["words"].apply(literal_eval)#Necessary step to recognize the list of string

words=df_words.index.tolist()
len_words=len(words)
filling=np.zeros((len_words,len_words), dtype=int)
df_adjacency_matrix=pd.DataFrame(filling, columns=words)

df_adjacency_matrix["Index_incoming"]=words
df_adjacency_matrix=df_adjacency_matrix.set_index("Index_incoming")

# length=df_tweets["words"].count()
# current=0

for index, value in df_tweets["words"].iteritems():#It is a series not a dataframe => iteritems instead of iterrows
    # current+=1
    # print(str(current/length*100)+" % done")
    a=value
    b=value
    for i in a:
        for j in b:
            # print(i, j)
            if i!=j:
                try:
                    df_adjacency_matrix.loc[i,j]+=1
                except KeyError:#We shortened the word list, so it will happend quite often (but not often enough to check with isin)
                    pass


elapsed = time.time() - start
min= int(elapsed/60)
sec=int(elapsed%60)
print("required "+str(min)+" min and "+str(sec)+" sec to process")


df_adjacency_matrix.to_csv(r".\3.Word Matrices\WordsAdjacencyMatrix.csv")
df_adjacency_matrix.to_excel(r".\3.Word Matrices\WordsAdjacencyMatrix.xlsx")

df_words.to_csv(r".\3.Word Matrices\WordsFrequencyShortened.csv")
df_words.to_excel(r".\3.Word Matrices\WordsFrequencyShortened.xlsx")