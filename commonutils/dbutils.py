from db import mongobase
from constants import dbconstants


def get_mongodb_connection(uri=dbconstants.LOCAL_MONGO_HOSTNAME, port_no=dbconstants.LOCAL_MONGO_PORT, db_name=dbconstants.DB_NAME):
    mongo = mongobase.MongoConnector(uri,port_no)
    mongo.set_db(db_name)
    return mongo
