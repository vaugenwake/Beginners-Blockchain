import asyncio

import structlog

logger = structlog.getLogger(__name__)


class P2PError(Exception):
    pass


class P2PProtocol:
    def __init__(self, server):
        self.server = server
        self.blockchain = server.blockchain
        self.connection_pool = server.connection_pool

    # Sends a message to a particular peer (the writer object)
    def send_message(writer, message):
        pass

    # Handles incoming message passed by the server
    def handle_message(self, message, writer):
        pass

    # Handles incoming "ping" message
    def handle_ping(self, message, writer):
        pass

    # Handles in coming "block" message
    def handle_block(self, message, writer):
        pass

    # Handles incoming "transaction" message
    def handle_transaction(self, message, writer):
        pass

    # Handles incoming "peers" message
    def handle_peers(self, message, writer):
        pass
