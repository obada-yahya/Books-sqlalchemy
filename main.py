from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    author = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=False)


def get_data():
    return db.session.query(Book).all()


@app.route("/edit/<int:num_id>", methods=["POST", "GET"])
def edit(num_id):
    book = Book.query.filter_by(id=num_id).first()
    if request.method == "POST":
        rating = float(request.values.get("rating"))
        book.rating = rating
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", book=book)


@app.route("/delete/<int:num_id>")
def delete(num_id):
    book = Book.query.get(num_id)
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


@app.route('/')
def home():
    global all_books
    all_books = get_data()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        title = request.values.get("title")
        author = request.values.get("author")
        rating = float(request.values.get("rating"))
        new_book = Book(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect("/")
    return render_template("add.html")


all_books = get_data()
db.create_all()


if __name__ == "__main__":
    app.run()
