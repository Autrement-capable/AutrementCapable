from fastapi import APIRouter
from fastapi import Depends, Path
from sqlmodel import Session
from pydantic import BaseModel
from config.server import AddRouter, server
from database.postgress.models.example import Example

example_router = APIRouter(prefix="/example", tags=["Example"])

@example_router.get("/")
def example(DB: Session = Depends(server.get_Psession), exapmle_id: int = Path(..., title="The ID of the example")):
    example = DB.get(Example, exapmle_id)
    if not example:
        return {"message": "Example not found"}
    return example.model_dump_json()

class ExampleForm(BaseModel):
    name: str
    username: str
    email: str
    password: str

@example_router.post("/")
def create_example(form: ExampleForm, DB: Session = Depends(server.get_Psession)):
    try:
        example = Example(name=form.name, username=form.username, email=form.email, password=form.password)
        DB.add(example)
        DB.commit()
        return example.model_dump_json()
    except Exception as e:
        return {"message": str(e)}, 400
    
AddRouter(example_router) # Add the router to the server