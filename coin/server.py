from asyncio import StreamReader, StreamWriter, IncompleteReadError
from marshmallow.exceptions import MarshmallowError
import asyncio
import coin.utils

from coin.messages import BaseSchema
from coin.blockchain import Blockchain
from coin.connections import ConnectionPool
from coin.peers import P2PProtocol

import structlog

logger = structlog.getLogger()


class Server:

    def __init__(self, blockchain: Blockchain, connection_pool: ConnectionPool, p2p_protocol: P2PProtocol):
        self.blockchain = blockchain
        self.connection_pool = connection_pool
        self.p2p_protocol = p2p_protocol
        self.external_ip = None
        self.external_port = None

        if not (blockchain and connection_pool and p2p_protocol):
            logger.error(
                "'blockchain', 'connection_pool', and 'gossip_protocol' must all be instantiated"
            )

            raise Exception("Could not start")

    async def get_external_ip(self):
        self.external_ip = await coin.utils.get_external_ip()

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        while True:
            try:
                # Wait for new messages to be recieved (potental DDoS risk)
                data = await reader.readuntil(b"\n")

                decoded_data = data.decode("uft8").strip()

                logger.info(decoded_data)

                # Validate the decoded message matches and expected structure.
                try:
                    message = BaseSchema().loads(decoded_data)
                except MarshmallowError:
                    logger.error("Recieved unreadable message", peer=writer)
                    break

                # Extract the address from the message, add it to the writer object
                writer.address = message["meta"]["address"]

                # Add the peer to our connection pool
                self.connection_pool.add_peer(writer)

                # handle the message
                await self.p2p_protocol.handle_message(message, writer)

                await writer.drain()
                if writer.is_closing():
                    break

            except (IncompleteReadError, ConnectionError):
                logger.error("Something went wrong, closing peer connection")
                break

    async def listen(self, hostname='0.0.0.0', port=8888):
        server = await asyncio.start_server(self.handle_connection, hostname, port)
        logger.info(f"Server listening on {hostname}:{port}")

        self.external_ip = await self.get_external_ip()
        self.external_port = 8888

        async with server:
            await server.serve_forever()
