from coin.schemas.transaction import Transaction
from time import time
import json

from marshmallow import Schema, fields, validates_schema, ValidationError


class Block(Schema):
    miner = fields.Str(required=False)
    transactions = fields.Nested(Transaction(), many=True)
    height = fields.Int(required=True)
    target = fields.Str(required=True)
    hash = fields.Str(required=True)
    previous_hash = fields.Str(required=True)
    nonce = fields.Int(required=True)
    timestamp = fields.Int(required=True)

    class Meta:
        ordered = True

    # Recalulate the blocks hash to verify if it is correct to be added to the chain
    @validates_schema
    def validate_hash(self, data, **kwargs):
        block = data.copy()
        block.pop("hash")

        if data["hash"] != json.dumps(block, sort_keys=True):
            raise ValidationError("Fraudulent block: hash is wrong")
