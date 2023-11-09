from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy

appLIBRI = Flask(__name__)

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

    if 'title' not in data:
        return jsonify({"error": "The 'title' field is required."}), 400

    try:
        new_book = Book(title=data['title'], author=data.get('author'))  # Author è un campo opzionale
        db_libri.session.add(new_book)
        db_libri.session.commit()
        return jsonify({"message": "Libro aggiunto"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appLIBRI.route('/get_books/<int:id>', methods=['GET'])
def get_books(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            return make_response(jsonify({'id': book.id}), 200)
        return make_response(jsonify({'message': 'Libro non trovato'}), 404)
    except:
        return make_response(jsonify({'message': 'Errore nel recupero dei libri'}), 500)

if __name__ == '__main__':
    appLIBRI.run(debug=True)
