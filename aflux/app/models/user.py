"""
Application models.

This classes are responsible for interacting
with the database. No authentication or business
logic is performed here.
"""

# pylint: disable=arguments-differ


import datetime

from app.models import mongo
from app.models.notification import Notification
from app.enum1 import USER_GENDER
from app.models.address import Address

class User(mongo.Document):
    """
    User model.
    """

    username = mongo.StringField(required=True, null=False, unique=True)
    password = mongo.StringField(required=True, null=False)
    created_at = mongo.DateTimeField(default=datetime.datetime.utcnow)
    notifications = mongo.EmbeddedDocumentListField(Notification)
    mobile_number = mongo.StringField(required=True, unique=True)
    is_mobile_number_verified = mongo.BooleanField(default=False)
    gender = mongo.StringField(max_length=1, choices=USER_GENDER)
    roles = mongo.ListField(mongo.StringField())

    selling_items = mongo.ListField(mongo.StringField())
    sold_items = mongo.ListField(mongo.StringField())
    owned_item = mongo.ListField(mongo.StringField())
    bought_item = mongo.ListField(mongo.StringField())

    # favor related (item_ids)
    num_favors = mongo.IntField(default=0, min_value=0)
    favor_items = mongo.ListField(mongo.StringField())

    addresses = mongo.ListField(mongo.ReferenceField('Address'))
    default_address = mongo.ReferenceField('Address')

    ID = "id"
    TIMESTAMP = "timestamp"
    USERNAME = "username"
    PASSWORD = "password"
    MOBILE = "mobile_number"
    MOBILE_VERIFIED = "is_mobile_number_verified"
    GENDER = "gender"
    ROLE = "roles"
    SELLING_ITEM = "selling_items"
    SOLD_ITEM = "sold_items"
    OWNED = "owned_item"
    BOUGHT_ITEM = "bought_item"
    NUM_FAVORS = "num_favors"
    FAVOUR_ITEM = "favor_items"
    ADDRESSES = "addresses"
    DEFAULT_ADDRESS = "default_address"

    meta = {
        'indexes': [{
            'fields': [
                '+created_at'  # Sorting key.
            ]
        }, {
            'fields': [
                '#username'  # Hash access key.
            ]
        }]
    }

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<User: '{}'>".format(self.pk)

    def get_id(self) -> str:
        """
        Instance ID getter.
        """
        return str(self.pk)

    def to_json(self) -> dict:
        """
        JSON serializer.
        """
        return {
            self.ID: self.get_id(),
            self.TIMESTAMP: str(self.created_at),
            self.USERNAME: self.username,
            self.PASSWORD: self.password,
            self.GENDER: self.gender,
            self.MOBILE: self.mobile_number,
            self.MOBILE_VERIFIED: self.is_mobile_number_verified,
            self.ROLE: self.roles,
            self.SELLING_ITEM: self.selling_items,
            self.BOUGHT_ITEM: self.bought_item,
            self.SOLD_ITEM: self.sold_items,
            self.OWNED: self.owned_item,

            self.NUM_FAVORS: self.num_favors,
            self.FAVOUR_ITEM: self.favor_items,
            self.ADDRESSES: self.addresses,
            self.DEFAULT_ADDRESS: self.default_address,

        }