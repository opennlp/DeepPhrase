from pykafka import KafkaClient
from config import keys


def get_kafka_producer(kafka_client=KafkaClient(hosts=keys.kafka['local_host_address']),topic_name='twitter_stream'):
    kafka_topic = kafka_client.topics[topic_name]
    kafka_producer = kafka_topic.get_producer()
    return kafka_producer
