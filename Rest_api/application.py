from flask import Flask, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=True, nullable=False)
    publisher = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.book_name} \n {self.author}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Books.query.all()

    output = []
    for book in books:
        book_data = {'book_name': book.book_name, 'book_author':book.author}

        output.append(book_data)

    print(output)
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Books.query.get_or_404(id)
    return {"book_name":book.book_name, 'book_author': book.author}

@app.route('/books', methods=['POST'])
def add_book():
    book = Books( book_name = request.json['book_name'],
                  author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id':book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Books.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "Done!"}

if __name__ == '__main__':
    app.run(debug=True)