from fastapi import Response
from config.db import engine
from db.schema.books import users
from starlette import status
import json
from typing import List
from functional import seq
import requests


class Users_repository:

#------------------------ CREATE USER--------------------------
    def create_user(self, user:dict): 
        try:  
            with engine.connect() as conn:
                new_book = users.insert().values(user)
                conn.execute(new_book)
                conn.commit()
                data = {"message": "User create successfully", "status_code": status.HTTP_201_CREATED}
                return Response(status_code=201,content=json.dumps(data), media_type="application/json")  
                   
        except Exception as e:
            data = {"message": "Error user not created: "+str(e), "status_code": status.HTTP_302_FOUND}
            return Response(status_code=302,content=json.dumps(data), media_type="application/json") 
    
    def get_user(self, email: str):
        try:
            with engine.connect() as conn:
                query = users.select().where(users.c.email.ilike(f"%{email}%"))
                results = conn.execute(query).fetchall()

                user_dict = seq(results).map(lambda result: {
                    "source": "Db Internal",
                    "id": result.id,
                    "name": result.name,
                    "email": result.email,
                    "password": result.password

                }).to_list()

                if user_dict:
                    return Response(status_code=200, content=json.dumps(user_dict), media_type="application/json")
                else:
                    data = {"message": "User not found", "status_code": status.HTTP_404_NOT_FOUND}
                    return Response(status_code=404, content=json.dumps(data), media_type="application/json")
        except Exception as e:
            data = {"message": "Error retrieving user: " + str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(status_code=500, content=json.dumps(data), media_type="application/json")