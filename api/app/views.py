"""
This module handles view routes

"""
# from instance.order_api import ManageOrders

from api.controller.order_api  import ManageOrders

class GetApiUrls(object):

    """
    class to define method to define all routes
    """
    def __init__(self):
        """class constructor"""


    @staticmethod
    def get_all_urls(APP):
        """function defining all the api routes """

        order_view = ManageOrders.as_view('order_api')

        APP.add_url_rule(
            '/api/v1/orders',
            defaults={
                'order_id': None
            }, view_func=order_view, methods=['GET',]
        )
        APP.add_url_rule('/api/v1/orders', view_func=order_view, methods=['POST',])

        APP.add_url_rule(
            '/api/v1/orders/<int:order_id>',
            view_func=order_view, methods=['GET', 'PUT']
        )
