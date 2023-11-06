from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 

##################################LIBRI#################################


appLIBRI = Flask(__name__)

appLIBRI.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@dbLIBRI/db_postgresLIBRI'

# DB
db_libri = SQLAlchemy(appLIBRI)


# Definisci il modello Book
class Book(db_libri.Model):
    __tablename__ = 'libri'
    id = db_libri.Column(db_libri.Integer, primary_key=True)
    title = db_libri.Column(db_libri.String(100), nullable=False)
    author = db_libri.Column(db_libri.String(100))
    def json(self):
        return {'Id': self.id, 'title': self.title, 'author': self.author}

with appLIBRI.app_context():
    db_libri.create_all()

# POST per aggiungere un libro
@appLIBRI.route('/add_book', methods=['POST'])
def add_book():
    data = request.get_json()
    
    if 'title' not in data:  # Assicurati che il campo "title" sia presente
        return jsonify({"error": "The 'title' field is required."})
    
    try:
        new_book = Book(title=data['title'], author=data['author'])  # author è un campo opzionale
        db_libri.session.add(new_book)
        db_libri.session.commit()
        return jsonify({"message": "Libro aggiunto"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Chiamata API per ottenere tutti i libri
@appLIBRI.route('/get_books', methods=['GET'])
def get_books():
    # Esegui una query per ottenere tutti i libri dal database
    books = Book.query.all()

    # Creare una lista di dizionari contenenti i titoli e gli autori dei libri
    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author
        }
        book_list.append(book_data)

    # Restituisci la lista di libri come risposta JSON
    return jsonify(book_list), 200

if __name__ == '__main__':
    appLIBRI.run(debug=True)
