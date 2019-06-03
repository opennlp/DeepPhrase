
def store_value(redis_client,key_name,value):
    redis_client.setnx(key_name,value)
    return True


def get_key_value(redis_client,key_name):
    return redis_client.get(key_name)
