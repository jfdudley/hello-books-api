from app import db



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", back_populates="books")
    genres = db.relationship("Genre", secondary="book_genre", backref="books")


    def to_dict(self):
        book_dict = {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description
        }

        if self.author:
            book_dict["author"] = self.author.name
        
        if self.genres:
            genre_names = [genre.name for genre in self.genres]
            book_dict["genres"] = genre_names
        
        return book_dict

# book_data_list = [
#     Book(9781912688036, "Band Sinister", "A strangely sexy romp through the English countryside that explores how an infamous heathen and uptight gentleman come together against all odds."),
#     Book(9781250831798, "A Marvellous Light", "Edwardian England full of magic, contracts, and conspiracies"),
#     Book(9781416903437, "Wild Magic", "A newly discovered young mage will have to learn to trust humans before she can come to terms with her powers, her past, and herself")
# ]