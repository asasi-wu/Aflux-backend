from datetime import datetime
from app.models import mongo


__all__ = ['Address']


class Address(mongo.Document):
    created_at = mongo.DateTimeField(default=datetime.utcnow)

    # address detail
    country = mongo.StringField(required=True)
    state = mongo.StringField(required=True)
    city = mongo.StringField()
    street1 = mongo.StringField()
    street2 = mongo.StringField()
    postcode = mongo.StringField()

    # receiver infomation
    receiver = mongo.StringField(required=True)
    mobile_number = mongo.StringField()

    def __unicode__(self):
        return '%s' % str(self.id)

    @property
    def fields(self):
        return ['country', 'state', 'city', 'street1', 'street2', 'postcode',
                'receiver', 'mobile_number']

    def to_json(self):
        result = {f: getattr(self, f) for f in self.fields}
        result.update({'id': str(self.id)})
        return result
