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
from connection import APP





class AuthorizeUsers(MethodView):
    """Class to define all the api end points"""
    
    def  post(self):
        APP.config['SECRET_KEY'] = 'thisissecret'
        rule = request.url_rule
        could_not_verify = {
            "Message":"Could not verify!"
        }
        if 'signup' in rule.rule:
            new_user_data = request.get_json()
            hashed_password = generate_password_hash(new_user_data['password'], method='sha256')

            """ insert a new user into the users table """

            sql = """INSERT INTO users(name,username,password,address,phone_number)
                    VALUES(%s,%s,%s,%s,%s) RETURNING user_id;"""
            return manage_users.execute_add_user_query(sql,
                new_user_data['name'],new_user_data['username'],hashed_password, 
                new_user_data['address'],new_user_data['phone_number']
            )
        #execute this block of code if its a login route
        auth = request.authorization
        if not auth or not  auth.password  or not auth.username:
            return make_response(json.dumps(could_not_verify), 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})
        else:
            return manage_users.execute_user_login_auth(auth.username, auth.password, could_not_verify)

                         
        
    def execute_user_login_auth(self, username, password,error_message):

        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s",(username, ))
            specific_user = cur.fetchall()
            user_exist = cur.rowcount
            if user_exist == 0:
                return make_response(json.dumps(error_message), 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})
            user_password = specific_user[0][3]
            if check_password_hash(user_password, password):
                user_username = specific_user[0][2]
                token = jwt.encode({'username':user_username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, APP.config['SECRET_KEY'])
                cur.close()
                return jsonify({'token generated':token.decode('UTF-8')}) 
            return make_response(json.dumps(error_message), 401, {'WWW-Authenticate' : 'Basic realm="Login required"'}) 
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    
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
            cur.execute(sql, (name, username, password, address, phone_number,))
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