from pykafka import KafkaClient
from config import keys
from pykafka import common


def get_kafka_consumer(kafka_client=KafkaClient(hosts=keys.kafka['local_host_address']), topic_name=keys.kafka['twitter_topic_name'],consumer_group_name='twitter_search'):
    topic = kafka_client.topics[topic_name]
    kafka_consumer = topic.get_simple_consumer(consumer_group=consumer_group_name,auto_offset_reset=common.OffsetType.EARLIEST,auto_commit_enable=False)
    return kafka_consumer


