from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from uuid import UUID,uuid4

app=FastAPI()

todos=[]

class Todo(BaseModel):
    id:UUID=Field(default_factory=uuid4)
    title:str
    iscompleted:bool


class TodoUpdate(BaseModel):
    title: str
    iscompleted: bool


@app.post("/todos")
def create_todo(todo:Todo):
    todos.append(todo)
    return {"message" : "Todo added","data":todo}

@app.get("/todos")
def get_todos():
    return todos

@app.get("/todo/{todo_id}")
def get_todo(todo_id: UUID):
    for todo in todos:
        if todo_id == todo.id:
            return todo

    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}")
def update_todo(todo_id: UUID, updated_todo: TodoUpdate):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = Todo(
                id=todo.id,
                title=updated_todo.title,
                iscompleted=updated_todo.iscompleted
            )

            return {
                "message": "Data Updated",
                "data": todos[index]
            }

    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:UUID):
    for index,todo in enumerate(todos):
        if todo.id==todo_id:
            todos.pop(index)
            return {"message":"delete successfully"}


    raise HTTPException(status_code=404, detail="Todo not found")