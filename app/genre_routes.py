from app import db
from app.models.genre import Genre
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request

genres_bp = Blueprint("genre_bp", __name__, url_prefix="/genres")

def validate_genre(genre_id):
    try:
        genre_id = int(genre_id)
    except:
        abort(make_response({"message":f"Genre {genre_id} is invalid."}, 400))
    
    genre = Genre.query.get(genre_id)

    if not genre:
        abort(make_response({"message":f"Genre {genre_id} not found."}, 404))
    
    return genre

@genres_bp.route("", methods=["POST"])
def create_genre():
    request_body = request.get_json()
    new_genre = Genre(name=request_body["name"])

    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify(f"Genre {new_genre.name} successfully created."), 201)

@genres_bp.route("", methods=["GET"])
def get_all_genres():
    genre_list = []
    genres = Genre.query.all()
    for genre in genres:
        genre_list.append(
            {
                "id" : genre.id,
                "name" : genre.name
            }
        )
    return jsonify(genre_list)

@genres_bp.route("/<genre_id>", methods=["GET"])
def get_one_genre(genre_id):
    genre = validate_genre(genre_id)

    return {
        "id" : genre.id,
        "name" : genre.name,
    }

@genres_bp.route("/<genre_id>", methods=["PUT"])
def update_genre(genre_id):
    genre = validate_genre(genre_id)

    request_body = request.get_json()

    genre.title = request_body["title"]
    genre.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Genre #{genre.name} successfully updated."))

@genres_bp.route("/<genre_id>", methods=["DELETE"])
def delete_genre(genre_id):
    genre = validate_genre(genre_id)

    db.session.delete(genre)
    db.session.commit()

    return make_response(jsonify(f"Genre #{genre.name} successfully deleted."))


# Nested Routes

@genres_bp.route("/<genre_id>/books", methods=["POST"])
def create_book(genre_id):

    genre = validate_genre(genre_id)

    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author_id=request_body["author_id"],
        genres=[genre]
    )
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@genres_bp.route("/<genre_id>/books", methods=["GET"])
def get_all_books(genre_id):
    genre = validate_genre(genre_id)

    books_response = []
    for book in genre.books:
        books_response.append(book.to_dict())
    
    return jsonify(books_response)

    