# schemas.py
from pydantic import BaseModel

class PersonalTextInput(BaseModel):
    title: str
    content: str

class QueryInput(BaseModel):
    query: str
