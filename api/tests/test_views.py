"""
This module contains test for the API end points
"""
import pytest
from flask import json
from api.controller.order_api import ManageOrders
from run import APP

APP = APP
CLIENT = APP.test_client
ORDER = ManageOrders()

def test_get_all_orders():
    """
    function to test get all orders API end point
    """
    result = CLIENT().get('/api/v1/orders')
    assert result.status_code == 200

@pytest.mark.parametrize("test_input, expected_output",
   [
       ("five", "The order id cannot be a String"),
       (True, "The order id cannot be a boolean")
   ]
   )
def test_get_specific_order_function(test_input, expected_output):
    """function to test get a specific  order API end point\
    such that a boolean nor a string  is not passed as a route parameter
    """
    with pytest.raises(TypeError):
        ORDER.get(test_input)




def test_if_parameter_passed_is_a_number_less_than_a_zero():
    """
    function to test get a specific  order API end point\
    such that an integer less than Zero is not passed as a route parameter
    """
    with pytest.raises(ValueError):
        ORDER.get(-1)



def test_if_data_posted_is_in_form_of_json():
    """
    function to test if data posted to the place order API is in form of Json
    """
    result = CLIENT().post(
        '/api/v1/orders', content_type='application/json',
        data=json.dumps(
            {
                "order_items": [
                    {
                        "item_id": 8,
                        "item_name": "Chips and Chicken",
                        "price": 50000,
                        "quantity": 3
                    }
                ],
                "user_id": 13
            }
        )
    )
    assert result.status_code == 201
    load_result_data = json.loads(result.data)
    assert 'order_items' in load_result_data
    assert  load_result_data['order_items'][0]['item_name'] == "Chips and Chicken"
    assert  load_result_data['order_items'][0]['price'] == 50000
    assert  load_result_data['order_items'][0]['quantity'] == 3
    assert  load_result_data['order_status'] == None



#Tests for updating the order status
def test_update_specific_order():
    """function to test whether data passed to the update end point is \
    in form of a JSON format
    """
    result = CLIENT().put(
        '/api/v1/orders/1', content_type='application/json',
        data=json.dumps(
            {
                "order_status":"Decline"
            }
        )
    )
    assert result.status_code == 200
    # get updated order
    order = CLIENT().get('/api/v1/orders/1')
    assert order.status_code == 200
    #get json data
    json_data = json.loads(order.data)
    assert json_data['order']['order_status'] == "Decline"



def test_if_parameter_passed_to_the_put_function_is_a_string():
    """
    function to test get a specific  order API end point\
    such that a string is not passed as a route parameter
    """
    with pytest.raises(TypeError):
        ORDER.put("ten")



def test_if_parameter_passed_to_the_put_function_is_a_number_less_than_a_zero():
    """
    function to test get a specific  order API end point\
    such that an integer less than Zero is not passed as a route parameter
    """
    with pytest.raises(ValueError):
        ORDER.put(-1)



def test_if_parameter_passed_to_the_put_function_is_a_boolean():
    """function to test get a specific  order API end point\
    such that a boolean is not passed as a route parameter
    """
    with pytest.raises(TypeError):
        ORDER.put(True)
        