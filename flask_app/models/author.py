from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book
class Author:
    def __init__( self , data ):
        self.id= data['id']
        self.name = data['name']
        self.fav_books = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL('books_schema').query_db(query)
        authors = []
        for author in results:
            authors.append( cls(author) )
  
        return authors
    
    @classmethod
    def get_unfavorite_authors(cls,data):
        query = "SELECT * FROM authors where authors.id not in (select authors_id from favorites where books_id=%(id)s);"
        results = connectToMySQL('books_schema').query_db(query,data)
        authors = []
        for author in results:
            authors.append( cls(author) )
  
        return authors
    
    @classmethod
    def get_author_books(cls,data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.authors_id LEFT JOIN books ON books.id = favorites.books_id WHERE authors.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query,data)
        
        authors = cls(results[0])
        for row_from_db in results:
           
           data = {
               "id" : row_from_db["books.id"],
               "title" : row_from_db["title"],
               "num_of_pages" : row_from_db["num_of_pages"],
               "created_at" : row_from_db["books.created_at"],
               "updated_at" : row_from_db["books.updated_at"]
           }
           authors.fav_books.append( book.Book( data ) )
        return authors
    
    @classmethod
    def get_author_name(cls,data):
        query = "SELECT * FROM authors WHERE id = %(id)s"
        
        result = connectToMySQL('books_schema').query_db(query,data)
       
        return cls(result[0])
    
    @classmethod
    def del_dojo(cls,id):
        
        query = "DELETE FROM dojos WHERE id ="+str(id)
        
        result = connectToMySQL('books_schema').query_db(query)
        
        return result
    
    @classmethod
    def update_author(cls,data):
        query = "UPDATE authors SET name=%(name)s, updated_at=NOW() WHERE id = %(id)s;"
        result = connectToMySQL('books_schema').query_db(query,data)
        return result
    
    @classmethod
    def save_fav(cls, data ):
        query = "INSERT INTO favorites ( authors_id, books_id) VALUES ( %(authors_id)s , %(books_id)s);"
        return connectToMySQL('books_schema').query_db( query, data )        
    
    @classmethod
    def save(cls, data ):
        print("data",data)
        query = "INSERT INTO authors ( name, created_at, updated_at ) VALUES ( %(name)s , NOW() , NOW() );"
        return connectToMySQL('books_schema').query_db( query, data )        
