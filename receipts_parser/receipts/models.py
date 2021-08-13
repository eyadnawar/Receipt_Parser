#from django.db import models

import mongoengine
from mongoengine import Document, fields

mongoengine.connect(db='Leaf_Labs', host='mongodb+srv://<username>:<password>@cluster0.gutxm.mongodb.net/Leaf_Labs?retryWrites=true&w=majority', username='eyad-admin', password='select33')

# Create your models here.
class Receipts(Document):
    receipt_id = fields.StringField()
    receipt = fields.FileField()
    receipt_name = fields.StringField()
    num_of_blocks = fields.IntField()
    receipt_blocks = fields.ListField(fields.DictField())

    def to_json(self):
        return {
            "receipts_id": self.receipt_id,
            "receipt": self.receipt,
            "receipts_name": self.receipt_name,
            "num_of_blocks": self.num_of_blocks,
            "receipts_blocks": self.receipt_blocks
        }





