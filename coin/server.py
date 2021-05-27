from asyncio import StreamReader, StreamWriter
import asyncio
from coin.utils import get_external_ip

import structlog

logger = structlog.getLogger()


class Server:

    def __init__(self, blockchain, connection_pool, p2p_protocol):
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
        self.external_ip = await get_external_ip()

    def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        pass

    def get_external_ip(self):
        pass

    async def listen(self, hostname='0.0.0.0', port=8888):
        server = await asyncio.start_server(self.handle_connection, hostname, port)
        logger.info(f"Server listening on {hostname}:{port}")

        self.external_ip = await self.get_external_ip()
        self.external_port = 8888

        async with server:
            await server.serve_forever()