"""
Script #5
1)  Draw a visual representation of the adjajency matrix following a graph theory representation
2)  Use the Louvain method for community detection in order to cluster words used in a similar context
3)  Plot again the graph with colored clusters
4)  Propose a dendogram representation of the clustering
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import community as community_louvain
import networkx as nx
import plotly.figure_factory as ff
import plotly.io as pio

df_adjacency_matrix=pd.read_csv(r".\3.Word Matrices\WordsAdjacencyMatrix.csv",index_col=0)
df_words=pd.read_csv(r".\3.Word Matrices\WordsFrequencyShortened.csv",index_col=0)

# df_adjacency_matrix= df_adjacency_matrix.iloc[200:205,200:205]#Todo: To remove at the end
# df_adjacency_matrix= df_adjacency_matrix.iloc[200:250,200:250]#Todo: To remove at the end

# nodes_list=df_words.index.tolist()[200:205]
# nodes_list=df_words.index.tolist()[200:250]
nodes_list=df_words.index.tolist()
nodes_labels=dict(zip(nodes_list,nodes_list))


G = nx.from_pandas_adjacency(df_adjacency_matrix)
G.name = 'Graph from pandas adjacency matrix'
print(nx.info(G))
nx.draw(G, node_size=20, with_labels=True)
plt.show()

# compute the best partition
partition = community_louvain.best_partition(G,resolution=0.2)#Play with resolution (max=1.0) in order to get less (higher number) or more communities (clusters)


# draw the graph
plt.axis('off')

pos = nx.spring_layout(G) #Initial
# pos = nx.circular_layout(G)

# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=20,
                       cmap=cmap, node_color=list(partition.values()))#node_color follows a perceptually uniform color theme [https://matplotlib.org/examples/color/colormaps_reference.html]
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_labels(G, pos, nodes_labels, font_size=1, font_color='w')
plt.savefig(r".\4.Plots\graph.png", dpi=1000)
plt.show()

clusters=list(partition.values())
df_words["cluster_id"]=clusters #Todo: to uncomment when running with full size matrix
df_words.to_csv(r".\5.Vocabulary Lists\WordsFrequencyShortenedClustered.csv")
df_words.to_excel(r".\5.Vocabulary Lists\WordsFrequencyShortenedClustered.xlsx")

# #[Proposal] draw a dendogram
# dendogram = community_louvain.generate_dendrogram(G,resolution=0.2, part_init=partition)
# label_dendogram=np.asarray(nodes_list)
# array_dendogram=np.asarray([list(dendogram[0].values())])
#
# fig = ff.create_dendrogram(array_dendogram,labels=nodes_list)
# fig.update_layout(width=800, height=500)
# pio.write_image(fig, r".\4.Plots\dendogram.png",scale=10)
# # pio.write_image(fig, r".\4.Plots\dendogram.pdf")
# # pio.write_image(fig, r".\4.Plots\dendogram.svg")
# fig.show()