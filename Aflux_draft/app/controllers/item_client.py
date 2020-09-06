# -*- coding: utf-8 -*-
import datetime
import json

from flask import jsonify



import app.models as Models


from app.exceptions.form import InvalidIdentifierException
from app.controllers import Cache
from app.exceptions.not_found import UserNotFoundException
from app import config



class Item_clientController:

    @classmethod
    def favor_items(cls,session: dict):
        current_user = cls.get_by_id(session['id'])

        favor_items = current_user.favor_items
        return jsonify(message='OK', id_list=favor_items)

    @classmethod
    def get_by_id(cls, user_id: str) -> Models.User:
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
        users = Models.User.objects(pk=user_id)
        if not users:
            raise UserNotFoundException()
        cache.set_value(users[0], expires_in=config.CACHE_USER)
        return users[0]

    @classmethod
    def favors_count(cls,session: dict):
        current_user = cls.get_by_id(session['id'])

        favor_items = current_user.favor_items
        return jsonify(message='OK', count=len(favor_items))



    @classmethod
    def item_favor(cls, query: dict, session: dict):
        current_user = cls.get_by_id(session['id'])
        item = Models.Item.objects(item_id=query["item_id"]).first_or_404()
        id = item.item_id


        if id not in current_user.favor_items:
            current_user.favor_items.append(id)
            current_user.save()
            return jsonify(message='OK')
        else:
            return jsonify(message='you already marker this item')



    @classmethod
    def item_unfavor(cls, query: dict, session: dict):
        current_user = cls.get_by_id(session['id'])
        item = Models.Item.objects(item_id=query["item_id"]).first_or_404()
        id = item.item_id

        user = current_user
        if id in user.favor_items:
            user.favor_items.remove(id)
            user.save()
            return jsonify(message='OK')
        else:
            return jsonify(message="Failed, you didn't mark this item")