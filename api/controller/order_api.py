"""
This module defines api views

"""
from flask import json
from flask import jsonify
from flask import request
from flask import Response
from flask.views import MethodView
from api.models.orders import Orders


class ManageOrders(MethodView):
    """Class to define all the api end points"""

    orders = []

    def post(self):
        """funtion to place a new order"""
        posted_data = request.get_json()
        if('order_items' in posted_data and 'user_id' in posted_data):
            for order in self.orders:
                if order.__dict__['user_id'] == posted_data['user_id'] and order.__dict__['order_status'] is  None:
                    list_index = 0
                    for item in order.__dict__['order_items']:
                        if item['item_id'] == posted_data['order_items'][list_index]['item_id']:
                            item['quantity']  +=posted_data['order_items'][list_index]['quantity']
                            item['price'] += posted_data['order_items'][list_index]['price']
                            response = Response(json.dumps(order.__dict__), 201, mimetype="application/json")
                            response.headers['location'] = "/api/v1/orders/" + str(order.__dict__['order_id'])
                            return response
                        list_index += 1
            order = Orders(
                len(self.orders) + 1, request.json['order_items'],
                None, request.json['user_id']
            )
            self.orders.append(order)
            response = Response(json.dumps(order.__dict__), 201, mimetype="application/json")
            response.headers['location'] = "/api/v1/orders/" + str(order.__dict__['order_id'])
            return response
        order_object = "{'order_items':[{'item_id': 7,item_name': 'Pizza',\
        'price':30000,'quantity': 6}],'user_id': 23}"
        bad_order_object = {
            "error": "Bad Order Object",
            "help of the correct order object format":order_object
        }
        response = Response(
            json.dumps(bad_order_object),
            status=400, mimetype="appliation/json"
            )
        return response


    def get(self, order_id):
        """function to get a single order or to get all the orders"""
        if order_id is None:
            # return a list of orders
            if not self.orders:
                return jsonify({"Message":"No Order Entries"})
            return jsonify({'all orders':[order.__dict__ for order in self.orders]})
        return MANAGE_ORDER.validate_get_specific_order(order_id)



    def put(self, order_id):
        """function to update a specific  order"""
        # update a specific order
        if not isinstance(order_id, int):
             raise TypeError(
                'The order id cannot be a String'
            )
        else:
            return MANAGE_ORDER.refactor_put_specific_order(order_id)
           



    def validate_get_specific_order(self, order_id):
        """
        function to validate get order id
        """
        if isinstance(order_id, int):
            return MANAGE_ORDER.refactor_validate_specific_order_function(order_id)
        else:
            raise TypeError('The order id cannot be a String')


    def refactor_validate_specific_order_function(self, order_id):
        """function to reduce complexty on validating order id function"""
        message = {'Message':'No Order Found with Specified Order Id'}
        response = Response(json.dumps(message), status=404, mimetype="appliation/json")
        if not isinstance(order_id, bool):
            if not order_id < 0:
                for order in self.orders:
                    if order.__dict__['order_id'] == order_id:
                        return jsonify({'order':order.__dict__})
                return response
            else:
                raise ValueError('The order id can not be a number less than zero')
        else:
            raise TypeError('The order id cannot be a boolean')



    def refactor_put_specific_order(self, order_id):
        """
        function to validate update order Id
        """
        message = {'Message':'No Order Found with Specified Order Id'}
        response = Response(json.dumps(message), status=404, mimetype="application/json")
        if not isinstance(order_id, bool):
            if not order_id < 0:
                get_spefic_order = [
                    order.__dict__ for order in self.orders
                    if order.__dict__["order_id"] == order_id
                ]
                if not get_spefic_order:
                    return response
                for order in self.orders:
                    if order.__dict__["order_id"] == order_id:
                        order_json = request.get_json()
                        order.__dict__['order_status'] = order_json['order_status']
                return jsonify({'orders':[order.__dict__ for order in self.orders]})
            else:
                raise ValueError(
                    'The order id cannot be an interger less than a zero'
                )
        else:
            raise TypeError(
                'The order id cannot be a boolean'
            )



MANAGE_ORDER = ManageOrders()
