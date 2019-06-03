from persistence import storage_factory
from config import keys


class StorageHandler:
    def __init__(self, storage_type, kafka_topic_name=keys.kafka['news_topic_name']):
        self.storage_type = storage_type
        self.kafka_topic_name = kafka_topic_name
        self.connection_object = storage_factory.get_storage_client(storage_type)

    def persist_data(self, insertion_object):
        storage_factory.persist_data(self.connection_object, insertion_object, self.storage_type, self.kafka_topic_name)

    def close_connection(self):
        storage_factory.close_connection(self.connection_object, self.storage_type)

