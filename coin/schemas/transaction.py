from time import time

from marshmallow import Schema, fields


class Transaction(Schema):
    timestamp = fields.Int()
    sender = fields.Str()
    reciever = fields.Str()
    amount = fields.Int()
    signature = fields.Str()

    class Meta:
        ordered = True
