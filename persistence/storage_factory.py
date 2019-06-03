from redis import Redis
from commonutils import dbutils, queueutils
from constants import modelconstants, dbconstants
from inmemory import redisutils, keygen_utils
from pykafka import KafkaClient
from config import keys
import pickle


def get_storage_client(storage_type='db'):
    if storage_type.lower() == modelconstants.INMEMORY_STORAGE_TYPE:
        redis_client = Redis()
        return redis_client
    elif storage_type.lower() == modelconstants.QUEUE_STORAGE_TYPE:
        kafka_client = KafkaClient(hosts=keys.kafka['local_host_address'])
        return kafka_client
    else:
        mongo_client = dbutils.get_mongodb_connection()
        return mongo_client


def persist_data(connection_object, insertion_document, storage_type='db', kafka_topic_name=keys.kafka['news_topic_name']):
    if storage_type.lower() == modelconstants.DB_STORAGE_TYPE:
        connection_object.set_collection(dbconstants.COLLECTION_NAME)
        connection_object.insert_document(insertion_document)
    elif storage_type.lower() == modelconstants.INMEMORY_STORAGE_TYPE:
        unique_key = keygen_utils.get_unique_mapping_key(insertion_document)
        redisutils.store_value(connection_object, unique_key, insertion_document)
    else:
        topic = queueutils.get_kafka_topic(connection_object, topic_name=kafka_topic_name)
        with topic.get_producer() as producer:
            producer.produce(pickle.dumps(insertion_document))


def close_connection(connection_object, storage_type='db'):
    if storage_type.lower() == modelconstants.DB_STORAGE_TYPE:
        connection_object.close_connection()
    elif storage_type.lower() == modelconstants.INMEMORY_STORAGE_TYPE:
        pass
    else:
        pass

