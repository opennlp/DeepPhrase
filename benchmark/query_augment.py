class QueryBatchMetric:

    def __init__(self,iteration,metadata):
        self.iteration = iteration
        self.metadata = metadata
        self.results_fetched = []
        self.number_results = 0
        self.intent_keyphrase_dict = dict({})
        self.intent_top_keyphrase_dict = dict({})
        self.updated_keyphrase_list = []
        self.cluster_metric = None
        self.cluster_coherence = None
        self.cluster_purity = None

    def get_object_dict(self):
        object_dict = dict({'iteration': self.iteration,
                            'metadata': self.metadata,
                            'results_fetched_list': self.results_fetched,
                            'number_of_results': self.number_results,
                            'intent_specific_keyphrase_dict': self.intent_keyphrase_dict,
                            'intent_top_keyphrase_dict': self.intent_top_keyphrase_dict,
                            'updated_keyphrase_list': self.updated_keyphrase_list,
                            'cluster_metric': self.cluster_metric,
                            'cluster_coherence': self.cluster_coherence,
                            'cluster_purity': self.cluster_purity})
        return object_dict
