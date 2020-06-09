"""
Script #6
1)  Build unlabelled thematic vocabulary lists ranked by frequency usage
    Suppose the words clustering has already be done beforehand
"""

import pandas as pd
import numpy as np

df_words=pd.read_csv(r".\5.Vocabulary Lists\WordsFrequencyShortenedClustered.csv",index_col=0)

number_of_clusters=df_words["cluster_id"].max()+1
cluster_scores=np.zeros(number_of_clusters)#We will need a cluster score for each cluster in order to rank them by learning usefulness

#compute the weighted frequency score of each cluster
for i in range(len(cluster_scores)):
    cluster_i=df_words[abs(df_words["cluster_id"]-i)<0.1]
    cluster_scores[i]=cluster_i["frequency"].mean()

#function retrieving the cluster score based on the cluster_id
def get_cluster_score(cluster_id):
    return cluster_scores[cluster_id]

#Rank words by cluster score
number_of_words=df_words.shape[0]
word_cluster_score=np.zeros(number_of_words)

for i in range(number_of_words):
    current_cluster_id=df_words["cluster_id"].iloc[i]
    word_cluster_score[i]=get_cluster_score(current_cluster_id)

df_words["cluster_score"]=word_cluster_score

df_words.sort_values(by=['cluster_score'],ascending=False,inplace=True)


#Create vocabulary list in Excel files, 1 list per cluster
for i,j in zip(range(number_of_clusters),cluster_scores):
    current_df = df_words[abs(df_words["cluster_score"] - j) < 0.01]
    current_df = current_df.reset_index()
    current_df = current_df.rename(columns={"index":"Palabras en español"})
    current_df = current_df["Palabras en español"]
    current_df.to_csv(r".\5.Vocabulary Lists\Thematic Lists\$"+str(i)+".csv")
    current_df.to_excel(r".\5.Vocabulary Lists\Thematic Lists\$"+str(i)+".xlsx")