
from datetime import datetime

from app.models import mongo





__all__ = ['Item']

class Item(mongo.Document):


    owner = mongo.StringField()
    owner_id = mongo.StringField()
    item_id = mongo.StringField(primary_key=True) # id
    eth_token = mongo.StringField()
    ## price
    price = mongo.FloatField()
    primary_img = mongo.StringField()
    images = mongo.ListField(mongo.StringField())
    # basic information
    title = mongo.StringField()
    brand = mongo.StringField()
    condition = mongo.StringField()
    description = mongo.StringField(default='')
    made_in = mongo.StringField()
    #color = db.ListField(db.StringField())
    location = mongo.StringField()

    main_category = mongo.StringField()
    sub_category = mongo.StringField()
    sex_tag = mongo.StringField()
    tags = mongo.ListField(mongo.StringField())

    availability = mongo.BooleanField(default=True)
    state = mongo.StringField()
    sku=mongo.IntField()

    # time
    created_at = mongo.DateTimeField(default=datetime.utcnow)
    modified = mongo.DateTimeField()
    creator = mongo.StringField()

    OWNER = "owner"
    OWNER_ID = "owner_id"
    ITEM_ID = "item_id"
    ETH_TOKEN = "eth_token"
    PRICE = "price"
    PRIMARY_IMG = "primary_img"
    IMAGES = "images"
    TITLE = "title"
    BRAND = "brand"
    CONDITION = "condition"
    DESCRIPTION = "description"
    MADE_IN = "made_in"
    LOCATION = "location"
    MAIN_CATEGORY = "main_category"
    SUB_CATEGORY = "sub_category"
    SEX_TAG = "sex_tag"
    TAGS = "tags"
    AVAILABILITY = "availability"
    SKU = "sku"







    meta = {
        'indexes': [{
            'fields': [
                '+created_at'  # Sorting key.
            ]
        }]
    }




    def __unicode__(self):
        return '%s' % self.item_id

    def __repr__(self):
        return '%s' % self.item_id



    def get_id(self) -> str:
        """
        Instance ID getter.
        """
        return str(self.pk)

    def to_json(self) -> dict:
        """
        JSON serializer.
        """
        return{
            self.OWNER: self.owner,
            self.OWNER_ID: self.owner_id,
            self.ITEM_ID: self.item_id,
            self.ETH_TOKEN: self.eth_token,
            self.PRICE: self.price,
            self. PRIMARY_IMG: self.primary_img,
            self.IMAGES:self.images,
            self.BRAND:self.brand,
            self.CONDITION:self.condition,
            self.DESCRIPTION :self.description,
            self.MADE_IN :self.made_in,
            self.LOCATION :self.location,
            self.MAIN_CATEGORY:self.main_category,
            self.SUB_CATEGORY :self.sub_category,
            self.SEX_TAG :self.sex_tag,
            self.TAGS :self.tags,
            self.AVAILABILITY :self.availability,
            self.SKU : self.sku,
                    }





    @property
    def cart_fields(self):
        return ['item_id', 'title', 'primary_img', 'price']

    def to_cart(self):
        result = {f: getattr(self, f) for f in self.cart_fields}
        return result


    @mongo.queryset_manager
    def available_items(doc_cls, queryset):
        return queryset.filter(availability=True)

    @property
    def small_thumbnail(self):
        return self.primary_img[:23] + 'thumbnails/150x150/' + self.primary_img[23:]

    @property
    def large_thumbnail(self):
        return self.primary_img[:23] + 'thumbnails/400x400/' + self.primary_img[23:]

    @classmethod
    def create(cls, item):

        item = Item(**item).save()
        item_id = item.item_id

        return item_id

    
