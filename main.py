from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Connect to MySQL
db = pymysql.connect(host='localhost', user='root', password='mysql@123', database='book-collection')
cursor = db.cursor()

# Uncomment the next two lines if you need to create the table
# cursor.execute("CREATE TABLE books (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(250) NOT NULL, author VARCHAR("
#                "250) NOT NULL, rating FLOAT NOT NULL)")
# db.commit()

@app.route('/')
def home():
    # Retrieve books from the database
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template("index.html", books=books)

@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        book_name = request.form["book_name"]
        book_author = request.form["book_author"]
        rating = request.form["rating"]
        book_id=request.form["book_id"]

        # Insert book into the database
        cursor.execute("INSERT INTO books (`id`,`title`, `author`, `rating`) VALUES (%s, %s, %s, %s)",
                       (book_id, book_name, book_author, rating))
        db.commit()

        return redirect(url_for('home'))
    return render_template("add.html")

@app.route('/delete/<int:book_id>', methods=['POST','GET'])
def delete(book_id):

    # Delete book from the database
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    db.commit()

    return redirect(url_for('home'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        book_name = request.form["book_name"]
        book_author = request.form["book_author"]
        rating = request.form["rating"]
        book_id=request.form["book_id"]

        # Update book in the database
        cursor.execute("UPDATE books SET title = %s, author = %s, rating = %s WHERE id = %s",
                       (book_name, book_author, rating, book_id))
        db.commit()

        return redirect(url_for('home'))

    # # Retrieve book from the database
    # cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    # book = cursor.fetchone()
    return render_template("edit.html", )

if __name__ == "__main__":
    app.run(debug=True)