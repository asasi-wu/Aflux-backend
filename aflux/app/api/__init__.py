"""
Application API.

These classes are only responsible for authenticating
the request and handling exceptions on behalf of the client.
"""

# pylint: disable=invalid-name

from flask_restful import Api

from app.api.health import HealthResource
from app.api.users import UsersResource
from app.api.notifications import NotificationsResource
from app.api.messages import MessagesResource
from app.api.auth import AuthResource
from app.api.add_item import Add_itemResource
from app.api.favor_item import favor_itemResource
from app.api.unfavor_item import unfavor_itemResource
from app.api.creat_order import create_orderResource
from app.api.order import orderResource
from app.api.pay_the_order import PAY_orderResource

api = Api()
api.add_resource(AuthResource, "/v1/auth", "/v1/login", "/login", "/auth")
api.add_resource(UsersResource, "/v1/users", "/users")
api.add_resource(MessagesResource, "/v1/messages", "/messages")
api.add_resource(HealthResource, "/", "/v1/health", "/v1/check", "/health", "/check")
api.add_resource(NotificationsResource, "/v1/notifications", "/notifications")
api.add_resource(Add_itemResource, "/v1/add_item", "/add_item")

api.add_resource(favor_itemResource, "/v1/favor_item", "/favor_item")
api.add_resource(unfavor_itemResource, "/v1/unfavor_item", "/unfavor_item")
api.add_resource(create_orderResource,"/v1/order","/creat_order")
api.add_resource(orderResource,"/v1/order","/order")
api.add_resource(PAY_orderResource,"/v1/order","/pay_the_order")