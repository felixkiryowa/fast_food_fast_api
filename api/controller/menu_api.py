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

    def get(self):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # cur.execute("SELECT vendor_id, vendor_name FROM vendors WHERE vendor_id=%s ORDER BY vendor_name", (id, ))
            cur.execute("SELECT * FROM menu ORDER BY item_id")
            available_menu = cur.fetchall()
            columns = ('item_id','item_name', 'price', 'current_items')
            results = []
            for row in available_menu:
                results.append(dict(zip(columns, row)))
            return jsonify({'Available Menu':results})
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                           
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