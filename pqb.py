from fastapi import FastAPI,HTTPException
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
def updated_user(user:User,user_id=int,notify:bool=False):
    if user_id<len(users):
        users[user_id]=user

        return {
            "message":"updated",
            "notify":notify,
            "data":user
        }
    raise HTTPException(status_code=404, detail="User not found")