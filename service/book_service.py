from db.entity.books_entity import Book 
from repository.repo_book import Books_repository

class Service_books:
  
    repository_book = Books_repository() 

    def read_books(self, 
                   title: str,
                   subtitle: str, 
                   author: str,
                   category: str, 
                   published_date: str, 
                   publisher: str
                   ): 

        return self.repository_book.read_books(title, subtitle, author, category, published_date, publisher)

    def create_book(self, book:Book, source:str, selfLink:str): 

        try:
        # Validar los campos de tipo str
            if not all(isinstance(value, str) for value in [book.title, book.subtitle, book.author, book.category, book.publisher, book.description]):
                raise ValueError('All fields must be strings')
           
            if selfLink == None and source=="google":
                raise ValueError('selfLink not found, google api book requires it.')
            else:

                #url = self.repository_storage.set_file(book.image, "book/%s-%s" % (book.title, book.author))
                new_user =  {
                    "title" : book.title,
                    "subtitle" : book.subtitle,
                    "author" : book.author,
                    "category" : book.category or "",
                    "publisher" : book.publisher,
                    "publishedDate": book.publishedDate,
                    "description" : book.description,
                    "image" : book.image or "",
                    "state": 1
                }

                return self.repository_book.create_book(new_user,source,selfLink)
            
        except Exception as e:
            return str(e)


    def delete_book(self, ID:int):   
        try:
            return self.repository_book.delete_book(ID)
        except Exception as e:
            return str("Error: " + str(e))

    def api_OPEN_LIBRARY(self, title:str):
        return self.repository_book.api_OPEN_LIBRARY(title)
