import json
from flask import Blueprint, jsonify, abort, make_response
from .book_data import book_data_list

books_bp = Blueprint("", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET"])
def complete_book_list():
    book_list = []
    for book in book_data_list:
        book_list.append({
            "id" : book.id,
            "title" : book.title,
            "description" : book.description
        })
    return jsonify(book_list)

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"Book {book_id} is invalid."}, 400))
    for book in book_data_list:
        if book.id == book_id:
            return book
    abort(make_response({"message":f"Book {book_id} not found."}, 404))

@books_bp.route("/<book_id>", methods=["GET"])
def get_specific_book(book_id):
    book = validate_book(book_id)

    return {
        "id" : book.id,
        "title" : book.title,
        "description" : book.description
    }