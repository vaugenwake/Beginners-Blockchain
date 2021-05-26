import asyncio
from coin.peers import P2PProtocol
from coin.server import Server

from coin.blockchain import Blockchain
from coin.connections import ConnectionPool
from coin.peers import P2PProtocol

blockchain = Blockchain()
connection_pool = ConnectionPool()


server = Server(blockchain, connection_pool, P2PProtocol)


async def main():
    await server.listen()

asyncio.run(main())
