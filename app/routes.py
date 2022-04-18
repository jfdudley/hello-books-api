import json
from flask import Blueprint, jsonify
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