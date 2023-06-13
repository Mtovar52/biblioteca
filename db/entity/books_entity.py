from pydantic import BaseModel, validator
from typing import Optional


class Book(BaseModel):
    id: Optional[int]
    title: str
    subtitle: str
    author: str
    category: str
    publisher: str 
    publishedDate: str
    description: str
    image: Optional[str]
    state: Optional[int]

