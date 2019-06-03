
def get_kafka_topic(kafka_client, topic_name):
    topic = kafka_client.topics[topic_name]
    return topic
