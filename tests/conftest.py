import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.book import Book

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book",
                    description="I love oceans")
    mountain_book = Book(title="Flower Book",
                        description="It's springtime!")

    db.session.add_all([ocean_book, mountain_book])
    db.session.commit()