from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__( self , data ):
        self.id= data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.fav_authors = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in results:
            books.append( cls(book) )
  
        return books
    
    @classmethod
    def get_unfavorite_books(cls,data):
        query ="SELECT * FROM books where books.id not in (select books_id from favorites where authors_id=%(id)s) ;"
        results = connectToMySQL('books_schema').query_db(query,data)
        books = []
        for book in results:
            books.append( cls(book) )
  
        return books
    
    @classmethod
    def get_author_books(cls,data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.books_id LEFT JOIN authors ON authors.id = favorites.authors_id WHERE books.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query,data)
        books = cls(results[0])
        for row_from_db in results:
           
           data = {
               "id" : row_from_db["authors.id"],
               "name" : row_from_db["name"],
               "created_at" : row_from_db["authors.created_at"],
               "updated_at" : row_from_db["authors.updated_at"]
           }
           books.fav_authors.append( author.Author( data ) )
        return books
    
    @classmethod
    def get_book_name(cls,data):
        query = "SELECT * FROM books WHERE id = %(id)s"
        
        result = connectToMySQL('books_schema').query_db(query,data)
        print("result",result)
        return cls(result[0])
    
    @classmethod
    def del_book(cls,id):
        
        query = "DELETE FROM books WHERE id ="+str(id)
        
        result = connectToMySQL('books_schema').query_db(query)
        
        return result
    
    @classmethod
    def update_book(cls,data):
        query = "UPDATE books SET name=%(name)s, updated_at=NOW() WHERE id = %(id)s;"
        result = connectToMySQL('books_schema').query_db(query,data)
        return result
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO books ( title, num_of_pages, created_at, updated_at ) VALUES ( %(title)s ,%(num_of_pages)s, NOW() , NOW() );"
        return connectToMySQL('books_schema').query_db( query, data )        
