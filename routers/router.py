from fastapi import APIRouter, Depends
from db.entity.books_entity import Book 
from db.entity.user_entity import User 
from repository.repo_book import Books_repository
from service.user_service import Service_users
from service.book_service import Service_books
from typing import Optional, List

router = APIRouter()

@router.get("/books", response_model=List[Book])  #endPoint1, Consulta base interna y Api Google
async def read_books(
    title: str = None,
    subtitle: str = None,
    author: str = None,
    category: str = None,
    published_date: str = None,
    publisher: str = None
): 
    service = Service_books()
    result=service.read_books(title, subtitle, author, category, published_date, publisher)
    return result

@router.post("/books")  #endPoint2, Crear libro en db interna con info de Api Google books
async def create_book(data_book: Book, source: str, selfLink: Optional[str] = None):
    service = Service_books()
    result= service.create_book(data_book,source, selfLink)
    return result
   
@router.get("/booksOpen") #EndPoint3, consultar a la Api Open Library 
async def api_OPEN_LIBRARY(title: str):
    service = Service_books()
    result=service.api_OPEN_LIBRARY(title)
    return result

@router.delete("/books/{id}")
async def delete_book(id: int):
    repository = Books_repository()
    result = repository.delete_book(id)
    return result

##CREATE USER AND HASH PASSWORD
@router.post("/users")
async def user(data_user: User):
    service = Service_users()
    result= service.create_user(data_user)
    return result

#Search user
@router.get("/user")
def get_user(email: str):
    service = Service_users()
    result = service.get_user(email)
    return result