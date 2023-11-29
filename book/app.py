from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import logging

appLIBRI = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO)

appLIBRI.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@dbLIBRI/db_postgresLIBRI'

db_libri = SQLAlchemy(appLIBRI)



class Book(db_libri.Model):
    __tablename__ = 'libri'
    id = db_libri.Column(db_libri.Integer, primary_key=True)
    title = db_libri.Column(db_libri.String(100), nullable=False)
    author = db_libri.Column(db_libri.String(100))
    
    def json(self):
        return {'id': self.id, 'title': self.title, 'author': self.author}

with appLIBRI.app_context():
    db_libri.create_all()

@appLIBRI.route('/add_book', methods=['POST'])
def add_book():
    data = request.get_json()
    logging.info('Data: %s', data)

    if 'title' not in data:
        return jsonify({"error": "The 'title' field is required."}), 400

    try:
        new_book = Book(title=data['title'], author=data.get('author'))  
        db_libri.session.add(new_book)
        db_libri.session.commit()

        logging.info('Libro aggiunto: %s', new_book.json())
        return jsonify({"message": "Libro aggiunto"}), 201

    except Exception as e:
        logging.error('Errore: %s', str(e))
        return jsonify({"error": str(e)}), 500
    
@appLIBRI.route('/get_books/<int:id>', methods=['GET'])
def get_books(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            return make_response(jsonify(book.json()), 200)
        return make_response(jsonify({'message': 'Libro non trovato'}), 404)
    except Exception as e:
        logging.error('Errore: %s', str(e))
        return make_response(jsonify({'message': 'Errore nel recupero dei libri'}), 500)
    
@appLIBRI.route('/get_books', methods=['GET'])
def get_all_books():
    try:
        books = Book.query.all()
        return jsonify([book.json() for book in books]), 200
    except Exception as e:
        logging.error('Errore: %s', str(e))
        return jsonify({"error": str(e)}), 500

@appLIBRI.route('/update_book/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    logging.info('Data: %s', data)

    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            db_libri.session.commit()

            logging.info('Libro aggiornato: %s', book.json())
            return jsonify({"message": "Libro aggiornato"}), 200
        return make_response(jsonify({'message': 'Libro non trovato'}), 404)
    except Exception as e:
        logging.error('Errore: %s', str(e))
        return jsonify({"error": str(e)}), 500

@appLIBRI.route('/delete_book/<int:id>', methods=['DELETE'])
def delete_book(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            db_libri.session.delete(book)
            db_libri.session.commit()

            logging.info('Libro eliminato: %s', book.json())
            return jsonify({"message": "Libro eliminato"}), 200
        return make_response(jsonify({'message': 'Libro non trovato'}), 404)
    except Exception as e:
        logging.error('Errore: %s', str(e))
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == '__main__':
    appLIBRI.run(debug=True)
