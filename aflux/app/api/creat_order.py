import logging

from flask import request
from flask_restful import Resource


from flask_jwt_extended import jwt_required, get_jwt_identity

from app.controllers.order import OrderController
from app.exceptions import IguazuException
from app.worker.tasks import AsyncCreateUserTask

logger = logging.getLogger(__name__)


class create_orderResource(Resource):
    """
    Users endpoint.
    """

    JOB_ID = "job_id"
    USERS = "users"

   

    @jwt_required
    def post(self) -> dict:
        """
        Create user.

        The async backend can be easily switched between
        UsersController.create() and UsersController.async_create()
        """
        #try:
        response = OrderController.create_order(request.json, get_jwt_identity())
        #except IguazuException as error:
            #logger.exception("Create user | sf_error=%s", error)
            #return error.to_json()

        return response