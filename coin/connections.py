import structlog

from more_itertools import take

logger = structlog.getLogger(__name__)

"""
Maintains a network of connected peers
* Core peer-to-peer management layer
"""


class ConnectionPool:

    def __init__(self) -> dict:
        self.connection_pool = dict()

    """
    Boadcast message to peers
    :param <any> data
    :return void
    """

    def broadcast(self, message):
        for user in self.connection_pool:
            user.write(f"{message}".encode())

    """
    Decode and return string of new peer ip:port
    """
    @staticmethod
    def get_address_string(writer):
        ip = writer.address["ip"]
        port = writer.address["port"]
        return f"{ip}:{port}"

    """
    Add a new peer to the network
    :param writer <dict> peer to add to the network
    """

    def add_peer(self, writer):
        address = self.get_address_string(writer)
        self.connection_pool[address] = writer
        logger.info("Added new peer to pool", address=address)

    """
    Remove a peer from the network
    """

    def remove_peer(self, writer):
        address = self.get_address_string(writer)
        self.connection_pool.pop(address)
        logger.info("Removed peer from pool", address=address)

    """
    Return the number of actively connected peers on our network
    """

    def get_alive_peers(self, count):
        # TODO (Reader): Sort these by most active
        return take(count, self.connection_pool.items())
