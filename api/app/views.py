"""
This module handles view routes

"""
# from instance.order_api import ManageOrders

from api.controller.auth_api import AuthorizeUsers
from api.controller.menu_api import Menu
from api.controller.order_api import Orders

class OrderApiUrls(object):

    """
    class to define method to define all routes
    """
    def __init__(self):
        """class constructor"""


    @staticmethod
    def get_all_urls(APP):
        """function defining all the api routes """

        auth_view = AuthorizeUsers.as_view('auth_api')
        menu_view = Menu.as_view('menu_api')
        order_view = Orders.as_view('order_api')
        APP.add_url_rule('/api/v2/users/orders', view_func=order_view, methods=['POST',])
        APP.add_url_rule('/api/v2/orders/',  defaults={
                'order_id': None
            }, view_func=order_view, methods=['GET',])
        APP.add_url_rule('/api/v2/auth/login', view_func=auth_view, methods=['POST',])
        APP.add_url_rule('/api/v2/auth/signup', view_func=auth_view, methods=['POST',])
        APP.add_url_rule('/api/v2/menu', view_func=menu_view, methods=['POST',])
        APP.add_url_rule('/api/v2/menu', view_func=menu_view, methods=['GET',])

