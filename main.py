from flask import Flask, Blueprint, render_template, redirect, flash, request, url_for, session
from cs50 import SQL

main_app = Blueprint('main_app', __name__, static_folder='static', template_folder='templates')

db = SQL('sqlite:///bookclub.db')


#homepage
@main_app.route('/')
def homepage():
    reviews = db.execute('SELECT title FROM book_review ORDER BY Date DESC;')
    comments = db.execute('SELECT comment FROM comments ORDER BY Date DESC;')
    return render_template('homepage.html')
    

#displaying lists of books, authors, and reviews when clicked
@main_app.route('/books')
def display_books():
    list_of_books = db.execute('SELECT book_title FROM book_title ORDER BY book_title;')
    return render_template('display_contents.html')

@main_app.route('/authors')
def display_authors():
    list_of_authors = db.execute('SELECT name FROM authors ORDER BY name;')
    return render_template('display_contents.html')

@main_app.route('/reviews')
def dispaly_groups():
    list_of_reviews = db.execute('SELECT title FROM book_review ORDER BY title;')
    return render_template('display_contents.html')


#displaying review (when clicked)
@main_app.route('/reviews/<review_id>')
def display_review(review_id: int):
    show_review = db.execute('SELCET * FROM book_review WHERE id = ?;', review_id)
    
    if len(show_review)!=1:
        return render_template('page_not_fount.html')
  
    show_review = show_review[0]
    
    #displaying author info of the book for this review
    
    book_author = db.execute('SELECT name FROM authors JOIN book_review ON authors.id = book_review.author_id JOIN book_title ON book_review.title_id=book_title.id WHERE id = ?;', review_id)
    
    return render_template('display_content.html')

#displaying details of a book(when clicked)
@main_app.route('/books/<book_id>')
def display_book(book_id: int):
    book = db.execute('SELCET book_title, rating, year_of_publication, description, book_cover FROM book_title WHERE id = ?;', book_id)
    
    if len(book)!=1:
        return render_template('page_not_found.html')
    
    book = book[0]
    
    #displaying author's info and genre of this book
    
    genre = db.execute('SELECT genre FROM genre JOIN book_genre ON genre.id = book_genre.genre_id JOIN book_title ON book_genre.title_id = book_title.id WHERE id = ?);', book_id)
    author = db.execute('SELECT name FROM authors WHERE id IN(SELECT author_id FROM book_title WHERE id = ?);', book_id)
    return render_template('display_content.html')
   
   #dispalying author info (when clicked)
@main_app.route('/author/<author_id>') 
def display_author(author_id: int):
    show_author = db.execute('SELECT * FROM authors WHERE id=?;', author_id)
       
    if len(show_author)!=1:
        return render_template('page_not_found.html')
       
    show_author = show_author[0]
       
    #displaying books of this author 
     
    books_of_this_author = db.execute('SELECT book_title FROM book_title WHERE author_id = ?;', author_id)
    return render_template('display_content.html')

#search bar for books, reviews, authors
@main_app.route('/search', methods=['POST', 'GET'])
def search_bar():
    if request.method == 'Get':
        return render_template('search.html')
    
    search_books = request.form.get('seach_books', None)
    search_reviews = request.form.get('seach_reviews', None)
    search_authors = request.form.get('seach_authorss', None)
    
    #querying database
    query_books = db.execute('SELECT book_title FROM book_title WHERE book_title LIKE ?;', search_books)
    query_reviews = db.execute('SELECT title FROM book_review WHERE title LIKE ?;', search_reviews)
    query_authors = db.execute('SELECT name FROM authors WHERE name LIKE ?;', search_authors)
    return render_template('display_content.html')
    
    
if __name__ == '__main__':
     main_app.run(debug=True)
      