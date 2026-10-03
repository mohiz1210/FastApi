from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

users=[]
class User(BaseModel):
    name:str
    email:str
    password:str

class UserResponse(BaseModel):
    name:str
    email:str
    

@app.post("/users")
def create_user(user:User):
    users.append(user)

    return {
        "message":"User Created",
        "data":user
    }
@app.get("/users",response_model=list[UserResponse])
def get_user():

    return users
