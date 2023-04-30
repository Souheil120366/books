from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.book import Book
from flask_app.models.author import Author

@app.route("/books")
def books_list():
    books = Book.get_all()
    return render_template("books.html",books_list=books)

@app.route("/books/<int:book_id>")
def book_show(book_id):
    book_to_show = Book.get_author_books({'id':book_id})
    books = Book.get_book_name({'id':book_id})
    all_authors=Author.get_unfavorite_authors({'id':book_id})
    return render_template("book_show.html",books_list_author=book_to_show.fav_authors,book=books,authors=all_authors)

@app.route("/books/<int:id>/edit")
def book_edit(id):
    books = Book.get_book(id)
    return render_template("edit_book.html",book=books)

@app.route('/books/new')
def create_book():
    return render_template("books.html")

@app.route("/books/create",methods=['POST'])
def new_book():
    Book.save(request.form)
    return redirect('/books')

@app.route("/favorites/books",methods=['POST'])
def new_favorite_books():
    print('request from fav',request.form['books_id'])
    books_id=request.form['books_id']
    Author.save_fav(request.form)
    return redirect('/books/'+books_id)

@app.route("/books/<int:id>/update",methods=['POST'])
def update_book():
    Book.update_book(request.form)
    return redirect('/books')

@app.route("/delete_book/<int:id>")
def delete_book(id):
    Book.del_book(id)
    return redirect('/books')