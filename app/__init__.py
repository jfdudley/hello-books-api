from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_problem_set'
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
        # app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_problem_set_test'
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.book import Book
    from app.models.genre import Genre 
    from app.models.author import Author
    from app.models.book_genre import BookGenre

    from .book_routes import books_bp
    app.register_blueprint(books_bp)

    from .genre_routes import genres_bp
    app.register_blueprint(genres_bp)

    from .author_routes import authors_bp
    app.register_blueprint(authors_bp)
    
    return app