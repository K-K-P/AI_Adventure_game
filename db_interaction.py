"""Connecting to Cassandra DB
Creating DB history and buffer memory for LLM
Requires cassandra and langchain libraries"""

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
from langchain.memory import CassandraChatMessageHistory  # Class for placing chat history in the db
from langchain.memory import ConversationBufferMemory  # Wrapper around DB interface


def connect():
    """Connect to Cassandra DB via Datastax"""
    cloud_config = {
        'secure_connect_bundle': 'secure-connect-choose-your-adventure.zip'  # provide secure data (from Datastax DB)
        # file name depends on the name of the DB that You provide
    }

    with open("Choose_your_adventure-token.json") as f:
        secrets = json.load(f)  # as above, load json file downloaded from Datastax's DB connection tab
        # Again, json file name depends on how You named the DB

    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    row = session.execute("select release_version from system.local").one()
    if row:
        return session
    else:
        print("An error occurred.")


def create_history(session, keyspace: str):
    """Create chat message history"""
    return CassandraChatMessageHistory(
        session_id='msg_history',  # naming this chunk of data
        session=session,  # initialize the session
        keyspace=keyspace,  # name of the DB keyspace
        ttl_seconds=3600  # length of the data lifespan
    )


def create_buff_memory(chat_history):
    """Create buffer memory for a chat. Every iteration of the script may result in a different outcome"""
    return ConversationBufferMemory(
        memory_key='chat_history',
        chat_memory=chat_history
    )


if __name__ == '__main__':
    connect()