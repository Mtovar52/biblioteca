from db.entity.books_entity import Book 
from fastapi import Response
from config.db import engine
from db.schema.books import books
from starlette import status
import json
from functional import seq
import requests
import ast 


class Books_repository:

 #----------------- LIST BOOK by Title,  Query in internal database and Google Api-------------------#
    
    def read_books(self, 
                   title: str,
                   subtitle: str, 
                   author: str,
                   category: str, 
                   published_date: str, 
                   publisher: str):
        try:
            with engine.connect() as conn:
                
                query = books.select().where(books.c.state == 1)
                conditions = []
                
                if title:
                    query = query.where(books.c.title.ilike(f"%{title}%"))

                if subtitle:
                    query = query.where(books.c.subtitle.ilike(f"%{subtitle}%"))

                if author:
                    query = query.where(books.c.author.ilike(f"%{author}%"))

                if category:
                    query = query.where(books.c.category.ilike(f"%{category}%"))

                if published_date:
                    query = query.where(books.c.publishedDate.ilike(f"%{published_date}%"))

                if publisher:
                    query = query.where(books.c.publisher.ilike(f"%{publisher}%"))

                if conditions:
                    query = query.where(*conditions)

                results = conn.execute(query).fetchall()

                book_dict = seq(results).map(lambda result: {
                    "source": "Db Internal",
                    "id": result.id,
                    "title": result.title,
                    "subtitle": result.subtitle,
                    "author": result.author,
                    "category": result.category,
                    "publisher": result.publisher,
                    "publishedDate": result.publishedDate,
                    "description": result.description,
                    "image": result.image,
                    "state": result.state
                }).to_list()

                if not book_dict:
                    # Search in the Google Books API
                    google_books_api_url = "https://www.googleapis.com/books/v1/volumes"
                    params = {"q": f'intitle:{title}',"maxResults": 10}

                    response = requests.get(google_books_api_url, params=params)
                    if response.status_code == 200:
                        
                        google_books_dict = self.api_GOOGLE(response)    
                        book_dict.extend(google_books_dict)

                    data = {"status_code": status.HTTP_200_OK, "Data": book_dict}
                    return Response(status_code=200, content=json.dumps(data), media_type="application/json")

                data = {"status_code": status.HTTP_200_OK, "Data": book_dict}
                return Response(status_code=200, content=json.dumps(data), media_type="application/json")
        except Exception as e:
            data = {"message": "Error book not found: "+str(e),"is_ok": False, "status_code": status.HTTP_302_FOUND}
            return Response(status_code=302,content=json.dumps(data), media_type="application/json")
#------------------------ CREATE BOOK--------------------------
    def create_book(self, book:Book, source:str, selfLink:str): 
        try:
            new_book = None
            if source == "internal":
                new_book = books.insert().values(book) 

            elif source == "google":
                data = self.read_books_APIS(selfLink)
  
                if data is not None:
                    author_value = data.get("author", [])
                    category_value = data.get("category", [])
                    author = ', '.join(author_value) if author_value else ''
                    category = ', '.join(category_value) if category_value else ''
                    new_book = books.insert().values(
                        title=data["title"],
                        subtitle=data["subtitle"],
                        author=author,
                        category=category ,
                        publisher=data["publisher"],
                        publishedDate=data["publishedDate"],
                        description=data["description"],
                        image=data["imageLinks"],
                        state=1
                    )
                else:
                    raise Exception("Error: Book data not found")
            
            with engine.connect() as conn:
                conn.execute(new_book)
                conn.commit()
                data = {"message": "Book create successfully","is_ok": True, "status_code": status.HTTP_201_CREATED}
                return Response(status_code=201,content=json.dumps(data), media_type="application/json")         
        except Exception as e:
            data = {"message": "Error book not created: "+str(e),"is_ok": False, "status_code": status.HTTP_302_FOUND}
            return Response(status_code=302,content=json.dumps(data), media_type="application/json")       
################################################################################################################################
#----------------- DELETE BOOK -----------------#
    def delete_book(self, ID:int):        
        delete_book = books.update().where(books.c.id==ID, books.c.state==1).values(state=0) 
        try:
            with engine.connect() as conn:
                result = conn.execute(delete_book)
                if result.rowcount > 0:
                    conn.commit()
                    data = {"message": "Deleting book successfully", "status_code": status.HTTP_200_OK}
                    return Response(status_code=200,content=json.dumps(data), media_type="application/json") 
                elif result.rowcount == 0:
                    raise Exception
        except Exception as e:
            data = {"message": "Error deleting book, id not found", "status_code": status.HTTP_302_FOUND}
            return Response(status_code=302,content=json.dumps(data), media_type="application/json") 

################################################################################################################################
 #----------------- LIST BOOK APIS by ("identificador") -------------------#
    
    def read_books_APIS(self, selfLink: str):
        
        try:
            response = requests.get(selfLink)
            
            if response.status_code == 200:
                book_data = response.json()
                volume_info = book_data.get("volumeInfo", {})
                google_books_dict = {
                    "source": "Google Books",
                    "title": volume_info.get("title", ""),
                    "subtitle": volume_info.get("subtitle", ""),
                    "author": volume_info.get("authors"),
                    "category": volume_info.get("categories"),
                    "publisher": volume_info.get("publisher", ""),
                    "publishedDate": volume_info.get("publishedDate", ""), 
                    "description": volume_info.get("description", ""),
                    "imageLinks": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                }                

            return google_books_dict
        
        except Exception as e:
            print("Error, books not found correctly", e)
            return []


#######################################################################################
####################### api_GOOGLE (Consulta a volumenes de libros) ###################
    @staticmethod
    def api_GOOGLE(response):
        google_books = response.json().get("items", [])
        google_books_dict = []
        for book in google_books:
            book_info = book.get("volumeInfo", {})
            self_link = book.get("selfLink", "")
            book_dict = {
                "source": "GOOGLE BOOK API",
                "title": book_info.get("title", ""),
                "author": str(book_info.get("authors", [])),
                "description": book_info.get("description", ""),
                "subtitle": book_info.get("subtitle", ""),
                "category": str(book_info.get("categories", [])),
                "publisher": book_info.get("publisher", ""),
                "publishedDate": book_info.get("publishedDate", ""),
                "imageLinks": book_info.get("imageLinks", {}).get("thumbnail", ""),
                "selfLink": self_link,
            }
            google_books_dict.append(book_dict)
        return google_books_dict
    
#######################################################################################
####################### OPEN LIBRARY API (Consulta a volumenes de libros) ###################
    def api_OPEN_LIBRARY(self, title:str):
       
        url = f"https://openlibrary.org/search.json"
        params = {"title": title, "limit": 10}

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            docs = data.get("docs", [])
            books = []
            for doc in docs:
                book = {
                    "source": "Open Library",
                    "key": doc["key"],
                    "title": doc.get("title", ""),
                    "publishedDate": doc.get("publish_date", ""),    
                    "ISBN": doc.get("isbn", []),
                }
                books.append(book)
            return books
        else:
            return None