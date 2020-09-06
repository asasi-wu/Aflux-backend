import json
from flask import jsonify


import app.models as Models

import uuid
import boto3

from app.exceptions.form import InvalidIdentifierException
from app.controllers import Cache
from app.exceptions.not_found import UserNotFoundException
from app import config


class ItemController:

    AWS_ACCESS_KEY_ID = "AKIAJYQHJGFNOI2SWVKA"
    AWS_SECRET_ACCESS_KEY = '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'
    BUCKET_NAME = 'aufluxtestv1'




    @classmethod
    def is_admin(cls, session: dict):
        current_user = cls.get_by_id(session['id'])
        roles = current_user.roles
        if 'ADMIN' in roles:
            return True
        else:
            return False


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
    def not_null(cls,dic):
        result = {}
        for i in dic.keys():
            if dic[i] in [None, u"None", "", "null"]: continue
            else:
                result[i] = dic[i]
        return result

    @classmethod
    def bytes2s3(cls,image, aws_path):
        s3 = boto3.resource('s3',
                        aws_access_key_id = cls.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = cls.AWS_SECRET_ACCESS_KEY)
        try:
            s3.Bucket('aufluxtestv1').put_object(Key=aws_path, Body=image)

        except Exception as e:
            pass

    @classmethod
    def upload_new_item(cls, data, session: dict):
        assert isinstance(session, dict)
        user_img = data['file'].read()##################################################
        print(type(user_img))
        cls.bytes2s3(user_img, aws_path = 'auflux/15485/picture.jpeg')
        return jsonify(message="Failed", desc='aaa')

    @classmethod
    def add_item(cls, data: dict,user_imgs, session: dict):
        if cls.is_admin(session):

            if not data or not user_imgs:
                return jsonify(message="Failed", desc='Wrong format of data')

            uni_id = str(uuid.uuid1())

            n = 0
            for image in user_imgs:                 #check the number of the total images

                cls.bytes2s3(user_imgs[image].read(), aws_path='auflux/{}/picture{}.jpeg'.format(uni_id, n))
                n = n + 1

            data_temp = {}
            for key in data:
                data_temp[key] = data[key]

            data_temp["item_id"] = uni_id
            item_id = Models.Item.create(data_temp)
            return jsonify(message='OK', item_id=item_id, data=data_temp)

        else:
            return jsonify(message='False', error='Permission denied')