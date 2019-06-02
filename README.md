## DeepPhrase - A Framework for Using Neural Representations for Generating Intent-based Query Phrases

DeepPhrase is a generic framework for leveraging the power of Neural Representations for tuning query phrases and making them more compatible with user defined intent. Presently the framework supports a set of social channels (i.e. Twitter, Reddit) and news sources.
This is an important component of our [JourneysDataLayer](https://github.com/opennlp/JourneysDataLayer) backend, but can be used independently for a variety of user applications. Check out details about our [Journeys](https://github.com/opennlp/JourneysAILayer) application for more details about the project and its philosophy.

Apart from making the process of querying easy for end users we also provide connectors to persistence stores so that users can push the collected data and query phrases to the data store of their choice. Currently we support the following data storage options, with more connectors coming soon.

  - Databases - MongoDB
  - Inmemory Data Store - Redis
  - Queue - Apache Kafka


## System Architecture

![Image of System Architecture](https://i.ibb.co/k8b8kqL/System-architecture.png)

The framework is designed to make it easy to plug in several alternate algorithms at each stage of the pipeline. For example the user has the choice of selecting from a whole list of alternate word/sentence embedding algorithms. The choice of persistence store and the data source (i.e. social channels and new sources) is also configurable by a given user. The data flow in the system starts when the user provides the seed query phrase and intent-phrase dictionary as input to the phrase augmenter server. The server then uses a set of APIs to query the external servers and fetch the necessary data. Once the data is fetched from the external servers (i.e. Twitter, Reddit, News etc.) we pass it through our seed phrase updating algorithm which generates candidate query phrases to append to the seed phrase for each given intent. With this set of updated seed phrases the process is iteratively repeated to finally settle on a given set of phrases corresponding to a given intent. Additionally, the user has the option of storing this fetched data in a persistence store for future use or otherwise.

## System Features

Salient features of the system include the following - 

1. Support for multiple word/sentence embeddings, presently we support the following embeddings - 
    - Word2Vec
    - GloVe
    - FastText
    - Universal Sentence Encoder
2. Mutliple Connectors for data persistence - MongoDB, Redis, Apache kafka

3. Inbuilt Support for Concept Drift - users have the option to schedule the update to their query phrases so that we can naturally deal with the problem of concept drift.

![Concept Drift Image](https://i.ibb.co/McRwywP/Trump-Timeline.png)

The figure illustrates the change in word distribution for tweets related to Donald Trump. The seed phrase used in the figure is “donald trump” and the intent dictionary contains phrases related to 3 topics - politics, policy and media. As can be inferred from the figure there is a wide variation in the key phrases used in the tweets for a duration of 9 months, the tweets during the period of October to December 2018 mostly deal with votes and making America great again, whereas during the first quarter of 2019 the tweets have centered around the border wall with Mexico. More recently, they have focused on the Chinese trade war and the Huawei ban. It is this concept-drift which makes it non-trivial to use fixed query phrases for fetching data for a given topic. Our approach to remedy this problem involves scheduling regular executions of our seed phrase update algorithm so that our query phrases are always in an updated state. A better approach will be to explicitly model this concept-drift and update the query phrases only when drift is statistically significant, this is something which we would like to explore in the future.

## Steps to Install and Use

1. git clone the repository to your local system
2. Run the following command to install all dependencies - 
```markdown
pip install -r requirements.txt
```
3. Download the pretrained models from [here](https://tinyurl.com/y2mlnhdf)
4. Copy the models to the models folder in the repository
5. Add your API keys (for Twitter, Reddit and/or News API) in the file keys.py under the config package.

## Usage and Code

``` python

def augment_seed_phrase():
    channel_name_list = ["reddit"]
    seed_phrase_list = ["adobe photoshop"]
    intent_dict = dict({'design': "design creative",
                        "image": "edit layer filter image",
                        "photography": "photography tool"})
    cluster_algorithm_list = ["kmeans", "lda"]
    embedding_model_list = ["glove"]
    ngram_value = 3
    num_iterations = 10
    similarity_measure = 'cosine'

    for channel_name in channel_name_list:
        for clustering_algorithm in cluster_algorithm_list:
            for embedding_model in embedding_model_list:
                try:
                    generate_iterative_seed(channel_name=channel_name,
                                            seed_phrase_list=seed_phrase_list,
                                            intent_dict=intent_dict,
                                            num_iterations=num_iterations,
                                            ngram_value=ngram_value,
                                            cluster_algorithm=clustering_algorithm,
                                            embedding_model=embedding_model, 
                                            similarity_measure=similarity_measure,
                                            storage_type=modelconstants.QUEUE_STORAGE_TYPE)
                except Exception as e:
                    LOGGER.info("An exception occured in seed augment %s " % str(e))
                    


from periodicschedule import scheduleupdate
from constants import modelconstants

if __name__ == '__main__':
    scheduleupdate.update_scheduler(augment_seed_phrase, time_quantum_unit='minutes', time_quantum=30)
    
 ```

## Experimental Results

In order to qualitatively evaluate the efficacy of our phrase augmenting algorithm we decided to carry out a crowdsourcing experiment on Amazon Mechanical Turk, where the workers where asked to label a given post as either relevant or irrelevant to the user intent given the seed phrase and intent-phrase dictionary as the supplementary material. For the purpose of this experiment the seed phrase used is “adobe photoshop” and the intents revolve around the following topics – design, image, photography. Each post has been rated by three workers (rated as being relevant to the user intent or not i.e. binary classification) and the inter-rater reliability has been measured in terms of Fleiss’s Kappa. We have used Fleiss’s Kappa instead of Cohen’s Kappa as it generalizes well beyond two raters and accounts for the case when the ratings are done by random workers (which is almost always the case in a crowdsourced setting). The Fleiss’s Kappa is always in the range of 0 to 1, with values greater than 0.4 denoting some degree of agreement among raters. The baseline used for comparison is the case of using the vanilla seed phrase without our proposed augmenting algorithm. 


Vectorizer|Ratio of Improvement|Fleiss’s Kappa
--------- | --------------------------- | --------------
GloVe |	0.58 |	0.71
FastText |	0.56 |	0.67
Word2Vec |	0.57	| 0.77
Universal Sentence Encoder |	0.54	| 0.63

### Convergence Measures per Iteration Basis

<p float="left">
  <img src="https://i.ibb.co/p3cCSyL/wordlist.png" width="150" />
  <img src="https://i.ibb.co/H7LNrMN/figure-2.png" width="150" /> 
  <img src="https://i.ibb.co/4gzq8sd/figure-3.png" width="150" />
</p>

The first figure shows some sample phrases which are appended to the seed query phrase “adobe photoshop” after the first iteration (for Reddit), it can be clearly seen that each phrase is totally pertinent to a given intent. The next figure shows the change in calinski-harabasz index with every iteration for Reddit, results for all the embeddings have been juxtaposed to get a better view of how changing the underlying embedding reflects on the cluster compactness. It can be inferred from the figure that after 3-4 iterations the algorithm converges, irrespective of the sentence/word representation used. The last graph shows results for topic modeling under the same settings as for KMeans version of the algorithm, the coherence measure shown is the average of all coherence values of the topics.

### Cluster Visualization

<p float="left">
  <img src="https://i.ibb.co/FXVcRB1/Reddit-KMeans-Photoshop.png" width="150" />
  <img src="https://i.ibb.co/Cm310L0/Reddit-KMeans-Photoshop-2.png" width="150" /> 
  <img src="https://i.ibb.co/hXb4RMc/Reddit-KMeans-Photoshop-3.png" width="150" />
</p>

The series of figures illustrates the evolution of the clusters corresponding to each intent using the KMeans version of our algorithm. The channel under consideration is Reddit and the underlying word embedding is GloVe. The seed keyphrase is "adobe photoshop" and the intents revolve around 3 topics - design, image and photography. As can be seen from the figure at each iteration the clusters become more well organized and separated. The keywords converge after about 3-4 iterations. The visualizations have been made by using t-SNE to project the embeddings corresponding to the posts in a lower dimensional space.

## Roadmap

  * Add support for more neural representation models - BERT, ELMo, Doc2Vec, Flair and CoVe
  * Support more database backends like MySQL, CouchDB, Apache Cassandra
  * Add support for indexing the data into a ElasticSearch cluster
  * Model the concept-drift explictly using a GAN or AutoEncoder
  
### Support or Contact

We are always happy to receive feedback on ways to improve the framework. Feel free to raise a PR in case of you find a bug or would like to improve a feature. In case of any queries please feel free to reach out to [Rupak](mailto:rupak97.4@gmail.com)
