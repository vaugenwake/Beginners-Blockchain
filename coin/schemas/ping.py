from time import time

from marshmallow import Schema, fields


class Ping(Schema):
    block_height = fields.Int()
    peer_count = fields.Int()
    is_miner = fields.Bool()
