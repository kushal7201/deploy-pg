import mysql.connector as mysql
import psycopg2  # PostgreSQL connector
import json
from flask import make_response
from datetime import *
import jwt # for generating token
from config.config import db_config

class user():
    def __init__(self):
        try:
            self.con = psycopg2.connect(
                host=db_config["hostname"],
                user=db_config["username"],
                password=db_config["password"],
                dbname=db_config["database"],  # "database" in psycopg2
                port=db_config.get("port", 5432)  # Optional, default PostgreSQL port
            )
            print("Connection successful")

            self.con.autocommit = True  # Set autocommit mode
            self.cursor = self.con.cursor()  # psycopg2 doesn't have a `dictionary=True` option directly
        except Exception as e:
            print(f"Failed to connect to the database: {e}")

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        result = self.cursor.fetchall()
        if len(result)>0:
            # print(result)
            res = make_response({"payload":result},200)
            res.headers["Access-Control-Allow-Origin"] = "*"
            return res   # in json format
            # return result  # in json format
        else:
            return make_response({"message":"No data found!"}, 204)
        # return "This is the users page"
        # return json.dumps(result)  # in string

    def user_signup(self,data):
        print(data)
        self.cursor.execute(f"INSERT INTO USERS(firstname,lastname,email,phone,password) VALUES('{data['firstname']}','{data['lastname']}','{data['email']}','{data['phone']}','{data['password']}')")
        return make_response({"message":"User created successfully"},201)
    
    def user_login(self, data):
        # print(data)
        self.cursor.execute(f"SELECT firstname,lastname, phone, avatar, role_id FROM users WHERE email='{data['email']}' and password= '{data['password']}' ")
        result = self.cursor.fetchall()
        userdata = result[0]
        expiry = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(expiry.timestamp())
        payload = {
            "payload":userdata,
            "exp":exp_epoch_time  # exp should be only named for expiration time
        }
        jwtoken = jwt.encode(payload,"kushal",algorithm="HS256")
        print(jwtoken)
        return make_response({"token":jwtoken},200)
    
    def user_update(self,data):
        print(data)
        self.cursor.execute(f"UPDATE users SET firstname='{data['firstname']}', lastname='{data['lastname']}', email= '{data['email']}', phone='{data['phone']}', password='{data['password']}' WHERE id={data['id']}")
        if self.cursor.rowcount>0:
            return make_response({"message":"User details updated successfully"},201)
        else:
            return make_response({"message":"Nothing to change!"},202)
    
    def user_patch(self,data,id):
        # print(data,id)
        query = "UPDATE users SET "
        for key in data:
            query += f"{key}='{data[key]}', "

        query = query[:-2] + f" WHERE id={id}"

        self.cursor.execute(query)

        if self.cursor.rowcount>0:
            return make_response({"message":"User details updated successfully"},201)
        else:
            return make_response({"message":"Nothing to change!"},202)
    
    def user_delete(self,id):
        print(id)
        self.cursor.execute(f"DELETE FROM users WHERE id = {id} ")
        if self.cursor.rowcount>0:
            return make_response({"message":"User deleted successfully"},200)
        else:
            return make_response({"message":"User NOT found!"},202)
        
    def user_pagination(self,limit,page):
        start = (page*limit) - limit
        query = F"SELECT * FROM users LIMIT {start}, {limit}"
        print(query)

        self.cursor.execute(query)

        result = self.cursor.fetchall()
        if len(result)>0:
            res = make_response({"payload":result, "page_no":page, "limit":limit},200)
            return res   # in json format
            # return result  # in json format
        else:
            return make_response({"message":"No data found!"}, 204)
        
    def user_upload_avatar(self,uid,path):
        self.cursor.execute(f"UPDATE users SET avatar = '{path}' WHERE id = {uid}")
        if self.cursor.rowcount0:
            return make_response({"message":"File uploaded successfully"},200)
        else:
            return make_response({"message":"Upload failed!"},202)