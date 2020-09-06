from datetime import datetime

from app.models import mongo
from app.enum1 import PAY_METHOD
from app.enum1 import ORDER_status

class OrderInfo(mongo.Document):


    created_at = mongo.DateTimeField(default=datetime.utcnow)
    order_id = mongo.StringField(max_length=100, verbose_name='订单编号')
    pay_method = mongo.StringField(choices=PAY_METHOD, default=3, verbose_name='支付方式')
    order_status = mongo.StringField(choices=ORDER_status, default='待支付', verbose_name='订单状态')
    product_count = mongo.IntField(verbose_name='产品数量')
    product_price = mongo.FloatField(max_digits=10, decimal_places=2, verbose_name='总价格')
    transit_price = mongo.FloatField(max_digits=10, decimal_places=2, verbose_name='运费')
    item_id = mongo.StringField(verbose_name='商品id')
    #user = mongo.ForeignKey('user.User', verbose_name='用户')
    user_id = mongo.StringField(required=True, null=False)
    addr = mongo.ListField(mongo.ReferenceField('Address'))
    #addr = mongo.ForeignKey('user.UserAddress', verbose_name='地址')
    trance_num = mongo.StringField(max_length=100, default='', verbose_name='支付编号')


    USER_ID = "user_id"
    ORDER_ID = "order_id"
    ITEM_ID = "item_id"
    PRODUCT_PRICE = "product_price"
    ADDRESS = "addr"
 

    meta = {
        'indexes': [{
            'fields': [
                '+created_at'  # Sorting key.
            ]
        }, {
            'fields': [
                '#order_id'  # Hash access key.
            ]
        }]
    }




    def to_json(self) -> dict:
        """
        JSON serializer.
        """
        return{
            self.ADDRESS:self.addr,
            self.ITEM_ID: self.item_id,
            self.ORDER_ID:self.order_id,
            self.PRODUCT_PRICE:self.product_price,
            
            self.USER_ID : self.user_id,
                    }