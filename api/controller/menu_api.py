"""
This module defines api views

"""
import psycopg2
import datetime
import jwt
from database.config import config
from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from werkzeug.security import generate_password_hash ,check_password_hash
from functools import wraps


from flask import json
from flask import jsonify
from flask import request
from flask import Response
from flask.views import MethodView
from connection import APP





class Menu(MethodView):
    """Class to define all the menu api end points"""
    
    def  post(self):
            # Get send order
            new_order_data = request.get_json()
            """ insert a new menu item into the menu table """

            sql = """INSERT INTO menu(item_name,price,current_items)
                    VALUES(%s,%s,%s) RETURNING item_id;"""
            return manage_menu.execute_add_menu_item_query(sql,
                new_order_data['item_name'],new_order_data['price'],new_order_data['current_items']
            )

                           
    def execute_add_menu_item_query(self,sql,item_name,price,current_items):
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (item_name, price, current_items,))
            # commit the changes to the database
            conn.commit()
            return jsonify({'Message':'New Menu Item Has Been  Created'})
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        

manage_menu = Menu()