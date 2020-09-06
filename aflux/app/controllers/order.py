#from django.shortcuts import render,redirect
#from django.core.urlresolvers import reverse


from app.models.user import User
from app.models.item import Item
from app.models.order import OrderInfo
import datetime
from alipay import AliPay
from flask import jsonify
from app.security.login import Session
from app.exceptions.not_found import UserNotFoundException
from app.controllers import Cache
from app.exceptions.form import (InvalidIdentifierException,
                                 InvalidUsernameException)
from app import config
class OrderController:

    @classmethod
    def create_order(cls, query: dict, session: dict):
        
        current_user = cls.get_by_id(session['id'])
        #data_temp = {}

        addr = current_user.addresses
        pay_id = query["pay_method"]
        s_id = query["item_id"]
        order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(current_user.get_id())
        transition = 10
        total_count = 1


        '''
        data_temp["order_id"] = order_id
        data_temp["pay_method"] = pay_id
        data_temp["transit_price"] = transition
        data_temp["item_id"] = s_id
        '''

        p=Item.objects(item_id=s_id,availability=True).update_one(availability=False)
        if p==1:
            total_price = Item.objects(item_id=query["item_id"]).first_or_404().price
            new_order = OrderInfo(user_id=current_user.get_id(),order_id=order_id,item_id = s_id, pay_method=pay_id, transit_price=transition,addr=addr,product_count=total_count, product_price=total_price)
            new_order.save()
        # 想订单商品表中添加数据   
        # 更新销量、库存
       
        # 更新订单信息表中的数据

            return new_order.to_json()
        else:
            jsonify("message": fail)

    @classmethod
    def get_by_id(cls, user_id: str) -> User:
        """
        Business method to get user by ID.

        If the user is cached, it will be read from cache.
        Otherwise, it will be read from the database and,
        if it exists, it will be cached.
        """
        if not user_id or not isinstance(user_id, str):
            raise InvalidIdentifierException()
        cache = Cache(f"user-{user_id}")
        if cache.is_cached():
            return cache.get_value()  # type: ignore
        users = User.objects(pk=user_id)
        if not users:
            raise UserNotFoundException()
        cache.set_value(users[0], expires_in=config.CACHE_USER)
        return users[0]



    @classmethod
    def order_preview(cls, query: dict, session: dict):
        current_user = cls.get_by_id(session['id'])
        item = Item.objects(item_id=query["item_id"]).first_or_404()
        total_price = item.price
        total_count = 1
        addrs = current_user.addresses
        transition = 10
        total_pricewithtran = transition + total_price
        context = {
            'total_product': total_count,
            'total_price': total_price,
            'transition': transition,
            'total_pricewithtran': total_pricewithtran,
            'addrs': addrs,
        }

        return jsonify(context)



    @classmethod
    def orderpay(cls, query: dict, session: dict):
        current_user = cls.get_by_id(session['id'])
        app_private_key_string = open('\home\\jindong\\Desktop\\app_private_key.pem').read()
        alipay_public_key_string = open('\home\\jindong\\Desktop\\alipay_public_key.pem').read()
        order=OrderInfo.objects(order_id=query["order_id"]).first_or_404()
        # app_private_key_string == """
        #     -----BEGIN RSA PRIVATE KEY-----
        #     MIIEpAIBAAKCAQEAq1BQ0rNviAGkpdeTDOenW3Ht5nRGLnB89roS3D1oOT/YE9HAWChqYrUxY1QMs5dFouvOFkKg+2JtoxqjPiAKKHx9chahRLWSf6RhGgZ7fnJ5pQhPbnq6hkV3qf/blORLBuRdKZYbnTRL0GpbQnbTT1k5vB5kw7n2qbD3ZJhnRgbL4uqAjtwCQZngn01zu0sR4vje9bB+Wy5LM6ydgGqRzbtiHHNR3D4yFDNzdVibtETPtpr0pJ7OgVsV6xQ/dfysLJ4JFPk2OoZPGhj72EmWZm8II3mqTvbtRBPZ3NsHYnKL9gMWgMJZjlXAOYW7WQgqhfG+SupC3/YIImIMmostQwIDAQABAoIBAGY9y87EKlcoa+RSUT/NbXNE/m+gi1Yh6mKx0JnCyFYKhWHmt/2lOUDp1KzsN5xjNrsyMk/UuhDtwHMsbaqhIo7hJVkWqm7AUst9BjqrDb78gR7+Y7GS64lBIlbCDYHB8gkN94/fN2HOGUUshISZOCnOHYfpN8gcT1sc87kEv/XpE8m3l6wtj+ckMYdpvd9Frz1Y1PVUTraDSVDPHGe3EpqK+Cea3dbhnnl7HPVonJ31JagC67B7Hh869h4VP4xrx/nlEGpy7KWHxOibL/nsESZjvGzJ+wDwEHKKad5WD4wgR1n0K58XBGU22ZBAGpkub+apZ8Vqs/g9RMFwIGnXoIECgYEA4f8lrUgkVq2QSuLXifOFnaIo/z0+X5/GMhxGT2QFAMRZK/+flYuy7miAhVlr8bOMDD3r9bToImLWInSkcSiWa+vadGp90XxQcnFzRaKkqjWwSRDicSSI75h0BahCJ7+dlkjB3GTjjV2OQwcnpbvcjzBw3M+chyChlzVOoN5uXkECgYEAwg6uzg4CQ7+F0FSxNCjCk9OjfUR4ggDbav13CiW4brW9VAbUKHsyF06d3xxaS4NzBxM663ZDY40Nl3NnaS6fPKYTb5jzr53NfYQk+mi/lkhQnM/alKd7ChUjsO9yv7iCsNIFn4mETtLNdAALS8Q88BEUHGA/3kX7PncI+cwYcoMCgYEAgS0qCAX4X2MN2wAWW0/Ky/Noo5wKDvZwfywSNEbjZTDWF4QhX4VeXU92RsJ6JMmP/19VhDhHh4AfDcrGQ7gDYuSJFYnZKOh5wzB9xwvUO0Y84Ua5aBqN+wWVK7alObsZBFHKHYO9XYxgSIfKbb0XsPDrUguJWOOZ+agKrYD2bQECgYAHm1281A3ArBxJu1gq7EIcW1p4SZvTtMblHcRx0GK3bEZcqdvdLl8bTMihe1IKzb9PkrBnlH41w8y5mBuAowQ482WlpUBALRZmCi0M59hCwtjuHLO7ygjnr0Zz5B8CZvAwkDsKMvDNyjOljW7j7HBbFMBOEHPQebvMigv/BsIakwKBgQCvAzNwpHG+6XTfkTV7mJN3LCNcFw9AtSmuujPudphsWGuW3yIxP4vFKyMypYzp2nf0rTwPpOyAfHdL3tUmiQkn/sEetMlsutlgChWEMoJQ6kmDeTuyErlLhB2cTr92Z0gaEXmDgYwiaNGM9wPLQ0vfk9gTE421VifbZ4GBidJcKA==
        #     -----END RSA PRIVATE KEY-----
        # """
        #
        # alipay_public_key_string == """
        #     -----BEGIN PUBLIC KEY-----
        #     MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoaeZ2GgnSBE2x2oDhHbaBiQNyFWradUObJwiPbk1o1xdNrbWemZ/3agHDaVLRDfcgmXQcgcwM3Y+1Pp8m4lZZgh98Wi8gR19fosblxstvSiyVrOZCCTM9FWLbR9FK8yeBsS9moyvUrABXDz3EhUubc4K4abAfCLv5UMbEKhMkdJQT8+LvyjMMI5a+ivrGruuQbUwoIgm3NVwgggLt8sg6W7vJ+33FAKzrihuw0tPAsqJq3YPxSqrCJ+m8/s1J4vAUDcSb3wblo9RaUiac2c0xwzMUrr+U58PMMVZp3pOaLIN/wrNT36upbbN12zEM6WDSqg8A6+VhzLVlPyLtmZCbwIDAQAB
        #     -----END PUBLIC KEY-----

        alipay = AliPay(
            appid="2016102500754838",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        total_price = order.product_price+order.transit_price
        subject = "Aflux{id}".format(id=order_id)

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            # Decimal类型需要转化成字符串
            total_amount=str(total_price),
            subject=subject,
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return jsonify({'pay': pay_url})
        
        

# 查询订单状态状态
'''
def checkorder(request):
    user = request.user
    if not user.is_authenticated():
        return JsonResponse({'res': 0, 'msg': '用户未登录'})

    order_id = request.POST.get('order_id')
    if not order_id:
        return JsonResponse({'res': 1, 'msg': '无效的订单号'})
    try:
        order = OrderInfo.objects.get(user=user, order_id=order_id, order_status=1, pay_method=3)
    except OrderInfo.DoesNotExist:
        return JsonResponse({'res': 2, 'msg': '订单不存在'})
    # 调用支付宝查询接口
    app_private_key_string = open(BASE_DIR + '\\order\\app_private_key.pem').read()
    alipay_public_key_string = open(BASE_DIR + '\\order\\alipay_public_key.pem').read()
    alipay = AliPay(
        appid="2016102500754838",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    while True:
        response = alipay.api_alipay_trade_query(order_id)
        code = response.get('code')
        if code == '10000' and response['trade_status'] == 'TRADE_SUCCESS':
            order.trance_num = response.get('trade_no')
            order.order_status = 4
            order.save()
            return JsonResponse({'res': 3, 'msg': '支付成功'})
        elif code == '40004' or (code == '10000' and response['trade_status'] == 'WAIT_BUYER_PAY'):
            # 等待支付
            continue
        else:
            return JsonResponse({'res': 4, 'msg': '支付失败'})
            '''