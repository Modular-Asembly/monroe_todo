from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.Todo import Todo
from app.modassembly.database.sql.get_sql_session import get_sql_session
from pydantic import BaseModel

router = APIRouter()

class TodoResponse(BaseModel):
    id: int
    text: str
    is_complete: bool

    class Config:
        orm_mode = True

@router.get("/todos", response_model=List[TodoResponse])
def list_todos(is_complete: Optional[bool] = None, db: Session = Depends(get_sql_session)) -> List[TodoResponse]:
    """
    Retrieve all todo items from the database.
    
    - **is_complete**: Optional query parameter to filter todos by their completion status.
    - Returns a list of todos.
    """
    query = db.query(Todo)
    if is_complete is not None:
        query = query.filter(Todo.is_complete == is_complete)
    todos = query.all()
    return [TodoResponse(id=todo.id, text=todo.text.__str__(), is_complete=todo.is_complete) for todo in todos]
