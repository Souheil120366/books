from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route("/")
def index():
    return redirect('/authors')

@app.route("/authors")
def dojos_list():
    authors = Author.get_all()
    return render_template("authors.html",authors_list=authors)

@app.route("/authors/<int:author_id>")
def dojo_show(author_id):
    author_to_show = Author.get_author_books({'id':author_id})
    
    authors = Author.get_author_name({'id':author_id})
    all_books=Book.get_unfavorite_books({'id':author_id})
    return render_template("author_show.html",books_list_author=author_to_show.fav_books,author=authors,books=all_books)

@app.route("/authors/<int:id>/edit")
def dojo_edit(id):
    authors = Author.get_author(id)
    return render_template("edit_author.html",author=authors)

@app.route('/authors/new')
def create_author():
    return render_template("authors.html")

@app.route("/authors/create",methods=['POST'])
def new_author():
    Author.save(request.form)
    return redirect('/authors')

@app.route("/favorites/authors",methods=['POST'])
def new_favorite_authors():
    print('request from fav',request.form['authors_id'])
    authors_id=request.form['authors_id']
    Author.save_fav(request.form)
    return redirect('/authors/'+authors_id)

@app.route("/authors/<int:id>/update",methods=['POST'])
def update_author():
    Author.update_author(request.form)
    return redirect('/authors')

@app.route("/delete_author/<int:id>")
def delete_author(id):
    Author.del_author(id)
    return redirect('/authors')