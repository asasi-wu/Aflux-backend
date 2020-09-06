# -*- coding: utf-8 -*-

class Enum(list):
    ''' Enumeration class '''
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    def __add__(self, other):
        # list addition
        result = super(Enum, self).__add__(other)
        return Enum(result)


class TupleEnum(list):
    '''
     Enumeration class expecting element as 2-tuple
    '''
    def __getattr__(self, name):
        keys = [k for k, v in self]
        if name in keys:
            return name
        raise AttributeError

    def __add__(self, other):
        # list addition
        result = super(TupleEnum, self).__add__(other)
        return TupleEnum(result)

    def __contains__(self, key):
        keys = [k for k, v in self]
        return key in keys


class DictEnum(dict):
    __getattr__ = lambda self, k: DictEnum(self.get(k)) if type(self.get(k)) is dict else self.get(k)


# user
USER_GENDER = Enum(['M', 'F'])



USER_ROLE = Enum(['MEMBER',
                  'ADMIN',
                  'CUSTOMER_SERVICE',
                  'OPERATION',
                  'MARKETING',
                  'TESTER',  # whose orders' final will always be 0.01
                  'LOGISTIC'])

USER_STATUS = Enum(['ACTIVE', 'INACTIVE', 'NEW'])

# item
ITEM_STATUS = Enum(['NEW', 'MOD', 'DEL'])
SEX_TAG = Enum(['MEN', 'WOMEN',
                'GIRLS', 'BOYS', 'INFANTS', 'TODDLERS', 'MOMS',
                'UNCLASSIFIED', 'UNKNOWN'])

# order
PAY_METHOD = Enum(['wechat', 'alipay', 'credit'])


ORDER_status = (['待支付', '代发货', '待收货', '待评价', '已完成'])




# tags
TAG_TYPES = TupleEnum([
    ('CATEGORY', 'tag of category type is used as level 3 category.'),
    ('MATERIAL', 'tag of material type denotes item materials.'),
    ('ELEMENT', 'tag of element type denotes special elements that the item contains.'),
    ('STYLE', 'tag of style type denotes the specific style of the item.')])


# refunds
REFUND_TYPE = Enum(['CANCEL', 'RETURN', 'SUBSIDY', 'MANUALLY'])

# report
REPORT_TYPE = Enum(['ORDER', 'LOGISTIC', 'ORDER_SOURCE', 'EXPENDITURE', 'IOS_SIGNUP_SOURCE',
                    'SHARE_LOG', 'REFUND'])

# POST
POST_STATUS = Enum(['NEW', 'MOD', 'DEL'])
ACTIVITY_STATUS= Enum(['PENDING', 'PROCESSED', 'REFUSED'])
POST_TAG_TYPES = Enum(['TRADE', 'SERVICE', 'SHOW', 'UNCLASSIFIED'])