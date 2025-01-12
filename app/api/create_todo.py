from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.Todo import Todo
from app.modassembly.database.sql.get_sql_session import get_sql_session

router = APIRouter()

class TodoCreate(BaseModel):
    text: str

class TodoResponse(BaseModel):
    id: int
    text: str
    is_complete: bool

    class Config:
        orm_mode = True

@router.post("/todos/", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_sql_session)) -> TodoResponse:
    """
    Create a new todo item.

    - **text**: The text description of the todo item.
    """
    db_todo = Todo(text=todo.text, is_complete=False)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return TodoResponse(id=db_todo.id.__int__(), text=db_todo.text.__str__(), is_complete=db_todo.is_complete.__bool__())
