
import logging

from flask import request
from flask_restful import Resource


from flask_jwt_extended import jwt_required, get_jwt_identity

from app.controllers.item import ItemController
from app.exceptions import IguazuException
from app.worker.tasks import AsyncCreateUserTask

logger = logging.getLogger(__name__)


class Add_itemResource(Resource):
    """
    Users endpoint.
    """

    JOB_ID = "job_id"
    USERS = "users"
    ITEM="item"

    @jwt_required
    def get(self) -> dict:
        """
        List items.
        """
        #try:
        items =ItemController.list_item(request.json, get_jwt_identity())
        #except IguazuException as error:
        #logger.exception("Listing users | sf_error=%s", error)
        #return error.to_json()
        #else:
        return {
                self.ITEM: [
                    item.to_json()
                    for item in items
                ]
            }
    @jwt_required
    def post(self) -> dict:
        """
        Create user.

        The async backend can be easily switched between
        UsersController.create() and UsersController.async_create()
        """
        #try:
        response = ItemController.add_item(request.form,request.files, get_jwt_identity())
        #except IguazuException as error:
            #logger.exception("Create user | sf_error=%s", error)
            #return error.to_json()

        return response
