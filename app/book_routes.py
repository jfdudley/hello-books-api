from app import db
from app.models.book import Book
from app.models.genre import Genre
from app.models.author import Author
from app.author_routes import validate_author
from app.genre_routes import validate_genre
from flask import Blueprint, jsonify, abort, make_response, request

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"Book {book_id} is invalid."}, 400))
    
    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message":f"Book {book_id} not found."}, 404))
    
    return book

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created."), 201)

@books_bp.route("", methods=["GET"])
def get_all_books():
    book_list = []
    books = Book.query.all()
    for book in books:
        book_list.append(book.to_dict())
    return jsonify(book_list)

@books_bp.route("/<book_id>", methods=["GET"])
def get_one_book(book_id):
    book = validate_book(book_id)

    return {
        "id" : book.id,
        "title" : book.title,
        "description" : book.description
    }

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book_id} successfully updated."))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book_id} successfully deleted."))


# Nested Routes

@books_bp.route("/<book_id>/author", methods=["POST"])
def add_author_to_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    if "id" in request_body:
        author = validate_author(request_body["id"])
    else:
        author = Author.query.filter_by(name=request_body["name"]).one()

    book.author = author

    db.session.commit()

    return jsonify(book.to_dict())

@books_bp.route("/<book_id>/genres", methods=["POST"])
def add_genre_to_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()
    if "id" in request_body:
        genre = validate_genre(request_body["id"])
    else:
        genre = Genre.query.filter_by(name=request_body["name"]).one()

    book.genres.append(genre)

    db.session.commit()

    return jsonify(book.to_dict())