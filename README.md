# RealSpanish
Proposing a new way to rank words to study in a foreign language by taking profit of use frequency and context-usage simultaneously

## Idea
I've always had the same problem  when learning the vocabulary of a new language:

**How to choose the most optimal words to study?**

To answer this question, there are two main schools:

1. Learning the vocabulary by theme with different vocabulary lists created by a human according to what he considers important. This method is usually the most popular one.
2. Learn the most used words based on frequency lists. For example, visit https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists

Both methods have advantages and weaknesses. Indeed, the former makes learning more interesting and easier, while the latter seeks efficiency at all costs. However, by doing so, the first method may lead you to learn "not so useful words" (Old-fashioned vocabulary, or just about a subject you are unlikely to be exposed to. Note that this can be interesting, but it is far from optimal if your goal is to use the language in everyday life). Regarding the frequency lists, the main problem is the fact the context is changing every line, making it painful to remember.

I was convinced a data science approach based on clustering could take the best of these two methods, so I decided to try it by myself. Results are given below.

## Results

Taking Spanish as example, the figure below present how I clustered words based on their context. On this graph, nodes represent Spanish words, and a edge is drawn between two words iff these two words are used in the same context. Although not shown on the graph, all edges are weighted.

![Internationalisation des entreprises wallonnes](https://github.com/pierre-crucifix/RealSpanish/blob/master/Results.png "Logo Title Text 1")

The graph figure is proposed in high-resolution, feel free to zoom in to read words.

After having done the clustering, I ranked the clusters based on a frequency score taking into account the frequency of each word in the cluster. The Spanish vocabulary lists obtained from applying the approach (presented in more details below) are given in the folder name *Thematic Vocabulary Lists*. Visually speaking, this means that we will first learn the words that are in the center of the graph, and the last lists will contain the ones that are on the periphery of the graph.

In that way, I have been able to propose thematic vocabulary lists taking profit of the words usage, i.e. I took the best of the two most popular schools presented at the beginning. The results are quite bluffing knowing they are based on unlabeled data. For example, we discover this algorithm has been able to group together regions (list #11), countries (list #13), time references (list #19) and days of the week (list #21). 

## Approach
*How does it work?*

The first sub-section presents briefly some implementation choices, and the second one gives the code structure.
### Implementation choices
The code is based on the Spanish language, but any written language can benefit from the method.
The text source is the 3,200+ latest tweets (16,157 tweets in total) of 5 main Spanish newspapers (4 focusing on general news, and 1 targeting business and economic news ; Twitter screen-names : @el_pais, @elmundoes, @abc_es, @LaVanguardia, @ExpansionMx). This choice is motivated by the fact we want good writers (with as few mistakes as possible) talking in a modern way.
Another option would be to use book content.

After cleaning, we obtain 25,000+ unique words. I decided to remove all words with less than 10 occurrences. In that way, we remove rare words but especially misspelled ones. We end the analysis on 3000+ words - a relevant quantity in a learning perspective.

Then, we build two matrices: a word frequency matrix and an adjacency one. Thanks to the adjacency matrix, we can take profit of graph theory by running the Louvain method for community detection. It is a clustering method based on modularity of nodes. More details about this clustering techniques can be found in this paper: https://arxiv.org/abs/0803.0476

In that way, we obtain the figure presented above, and we are able to create the vocabulary list by using the constructed optimal partition of the graph.

### Code structure
From scratch, scripts have to be used in the following order:

 1. *tweepyManager.py*
 2. *cleaner.py*
 3. *word_frequency_matrix_builder.py*
 4. *word_adjacency_matrix_builder.py*
 5. *plotter.py*
 6. *vocabulary_lists_builder.py*
 
 
 
<br/><br/>

*Author:* Pierre Crucifix
