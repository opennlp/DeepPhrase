## DeepPhrase - A Framework for Using Neural Representations for Generating Intent-based Query Phrases

DeepPhrase is a generic framework for leveraging the power of Neural Representations for tuning query phrases and making them more compatible with user defined intent. Presently the framework supports a set of social channels (i.e. Twitter, Reddit) and news sources.
This is an important component of our JourneysDataLayer backend, but can be used independently for a variety of user applications. Check out details about our Journeys application for more details about the project and its philosophy.

Apart from making the process of querying easy for end users we also provide connectors to persistence stores so that users can push the collected data and query phrases to the data store of their choice. Currently we support the following data storage options, with more connectors coming soon.

  - Databases - MongoDB
  - Inmemory Data Store - Redis
  - Queue - Apache Kafka


### System Architecture

![Image of System Architecture](https://github.com/opennlp/DeepPhrase/blob/master/System%20architecture.PNG)

The framework is designed to make it easy to plug in several alternate algorithms at each stage of the pipeline. For example the user has the choice of selecting from a whole list of alternate word/sentence embedding algorithms. The choice of persistence store and the data source (i.e. social channels and new sources) is also configurable by a given user. The data flow in the system starts when the user provides the seed query phrase and intent-phrase dictionary as input to the phrase augmenter server. The server then uses a set of APIs to query the external servers and fetch the necessary data. Once the data is fetched from the external servers (i.e. Twitter, Reddit, News etc.) we pass it through our seed phrase updating algorithm which generates candidate query phrases to append to the seed phrase for each given intent. With this set of updated seed phrases the process is iteratively repeated to finally settle on a given set of phrases corresponding to a given intent. Additionally, the user has the option of storing this fetched data in a persistence store for future use or otherwise




```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/opennlp/DeepPhrase/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
