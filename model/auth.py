from functools import wraps
import re
import mysql.connector as mysql
import psycopg2  # PostgreSQL connector
import json
from flask import make_response, request
import jwt # for generating token
from config.config import db_config

class auth():
    def __init__(self):
        try:
            self.con = psycopg2.connect(
                host=db_config["hostname"],
                user=db_config["username"],
                password=db_config["password"],
                dbname=db_config["database"],  # "database" in psycopg2
                port=db_config["port"],  # Optional, default PostgreSQL port
            )
            print("Connection successful")

            self.con.autocommit = True  # Set autocommit mode
            self.cursor = self.con.cursor()  # psycopg2 doesn't have a `dictionary=True` option directly
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            
            
        except:
            print("Connection ERRROR!") 

    def token_auth(self, endpoint=""):
        def m_func(og_func):
            @wraps(og_func)    # for solving problem of token_auth in multiple endpoints error
            def check(*args):
                endpoint = request.url_rule
                print(endpoint)
                auth = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$",auth, flags=0):
                    token = auth.split(" ")[1]
                    try:
                        jwt_decoded = jwt.decode(token,"kushal",algorithms="HS256")
                    except jwt.ExpiredSignatureError:
                        return make_response({"message":"Token expired"},201)

                    role_id = jwt_decoded['payload']['role_id']
                    self.cursor.execute(f"SELECT roles FROM accessibility_view WHERE endpoint = '{endpoint}'")
                    result = self.cursor.fetchall()
                    if len(result)>0:
                        alowed_roles = json.loads(result[0]['roles'])   # json.loads convert string into array
                        if role_id in alowed_roles:
                            return og_func(*args)
                        else:
                            return make_response({"message":"Access Denied!"},201)
                    else:
                        return make_response({"message":"Unknown ENDPOINT"},404)
                    
                else:
                    return make_response({"message":"INVALID_TOKEN"}, 401)

            return check
        return m_func
        