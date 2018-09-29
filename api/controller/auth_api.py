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
from api.models.users import Users


class AuthorizeUsers(MethodView):
    """Class to define all the api end points"""
    
    def  post(self):
        rule = request.url_rule

        if 'signup' in rule.rule:
            new_user_data = request.get_json()
            hashed_password = generate_password_hash(new_user_data['password'], method='sha256')

            """ insert a new user into the users table """

            sql = """INSERT INTO users(name,username,password,address,phone_number,admin)
                    VALUES(%s,%s,%s,%s,%s,%s) RETURNING user_id;"""
            return manage_users.execute_add_user_query(sql,
                new_user_data['name'],new_user_data['username'],hashed_password, 
                new_user_data['address'],new_user_data['phone_number']
            )
        return jsonify({"Message":"This a login route"})
        
       
    def execute_add_user_query(self,sql,name,username,password,address,phone_number):
        conn = None
        # user_id = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (name, username, password, address, phone_number ,False,))
            # commit the changes to the database
            conn.commit()
            return jsonify({'Message':'New User Account Has Been  Created'})
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        

manage_users = AuthorizeUsers()