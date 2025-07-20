from flask import Flask, render_template, request, redirect
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Add Book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']
        cursor.execute("INSERT INTO books (title, author, genre, price) VALUES (%s, %s, %s, %s)", (title, author, genre, price))
        db.commit()
        return redirect('/')
    return render_template('add_book.html')

# View Books
@app.route('/view')
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template('view_books.html', books=books)

# Update Book
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    if request.method == 'POST':
        # Handle form submission for updating the book
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']

        # Update the database with the new values
        cursor = db.cursor()
        cursor.execute("""
            UPDATE books 
            SET title = %s, author = %s, genre = %s, price = %s 
            WHERE id = %s
        """, (title, author, genre, price, id))
        db.commit()
        cursor.close()

        return redirect('/')
    
    # Render the update form (for GET request)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cursor.fetchone()
    cursor.close()

    if book:
        return render_template('update_book.html', book=book)
    else:
        return "Book not found", 404

# Delete Book
@app.route('/delete/<int:id>')
def delete_book(id):
    cursor.execute("DELETE FROM books WHERE id=%s", (id,))
    db.commit()
    return redirect('/view')

if __name__ == '__main__':
    app.run(debug=True)
