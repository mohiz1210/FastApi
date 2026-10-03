from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

users=[]
class User(BaseModel):
    name:str
    age:int

@app.post("/users")
def create_user(user:User):
    users.append(user)

    return {
        "message":"User Created",
        "data":user
    }

@app.put("/users{user_id}")
def updated_user(user_id=int,notify:bool=False,user:User)