

from flask import jsonify

from app.models.cart import Cart, CartEntry
from app.models.item import Item
from app.controllers.users import UsersController

class CartController:


    USER_ID = "user_id"

    ITEM_ID = "item_id"

    @classmethod
    def get_cart(cls, query: dict, session: dict):
        assert isinstance(session, dict)
        user = UsersController.get_by_id(query[cls.USER_ID])
        user_id = str(user.id)
        current_cart = Cart.get_cart_or_create(user_id)
        return current_cart

    @classmethod
    def add_to_cart(cls, query: dict, session: dict):
        assert isinstance(session, dict)
        current_cart = cls.get_cart(query, session)

        items = current_cart.entries

        if query[cls.ITEM_ID] in [i.item_id for i in items]:
            return jsonify(message='Failed, This item already has been add to your cart')
        else:
            if not Item.objects(item_id=query[cls.ITEM_ID]):
                return jsonify(message='Failed, item not exist')
            item = Item.objects(item_id=query[cls.ITEM_ID]).first_or_404()
            meta = item.to_cart()
            cart_entry = CartEntry(**meta)
            cart_entry.save()
            current_cart.entries.insert(0, cart_entry)
            current_cart.save()
            return jsonify(message='OK', cart_id=str(current_cart.id))


    @classmethod
    def remove_from_cart(cls, query: dict, session: dict):

        assert isinstance(session, dict)
        cart_entry = CartEntry.objects(item_id=query[cls.ITEM_ID]).first_or_404()
        current_cart = cls.get_cart(query, session)
        if cart_entry not in current_cart.entries:
            return jsonify(message='Failed',
                        error=('invalid item_id for current user'))
        current_cart.update(pull__entries=cart_entry)
        cart_entry.delete()
        return jsonify(message='OK')


    @classmethod
    def all_items_in_cart(cls, query: dict, session: dict):
        assert isinstance(session, dict)
        current_cart = cls.get_cart(query, session)
        items = current_cart.entries
        total_price=[]
        cart_content=[]
        for item in items:
            total_price.append(item.price)
            cart_content.append(item.to_json())
        return jsonify(message='OK', total_price=sum(total_price), cart_content=cart_content, count=len(total_price))