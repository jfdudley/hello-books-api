from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)


# book_data_list = [
#     Book(9781912688036, "Band Sinister", "A strangely sexy romp through the English countryside that explores how an infamous heathen and uptight gentleman come together against all odds."),
#     Book(9781250831798, "A Marvellous Light", "Edwardian England full of magic, contracts, and conspiracies"),
#     Book(9781416903437, "Wild Magic", "A newly discovered young mage will have to learn to trust humans before she can come to terms with her powers, her past, and herself")
# ]