from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy 
import logging
import os

log_file_path = os.path.abspath('app.log')
logging.basicConfig(filename=log_file_path, level=logging.DEBUG)

#################################UTENTI#############################
app = Flask(__name__)
 
# Configura la connessione al database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@dbutenti/db_postgres'


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Cambiato da 'unique=True'
    surname = db.Column(db.String(50), nullable=False)  # Cambiato da 'unique=True'

    def json(self):
        return {'id': self.id, 'name': self.name, 'surname': self.surname}
with app.app_context():
     db.create_all()

#POST
@app.route('/add_user', methods=['POST'])
def add_user():
    logging.info('POST /add_user')
    data = request.get_json()

    if 'name' not in data or 'surname' not in data:
        logging.error("Both 'name' and 'surname' fields are required.")
        return jsonify({"error": "Both 'name' and 'surname' fields are required."}), 400

    try:
        new_user = User(name=data['name'], surname=data['surname'])
        db.session.add(new_user)
        db.session.commit()
        logging.info("Utente aggiunto: %s %s", data['name'], data['surname'])
        return jsonify({"message": "Utente aggiunto"}), 200

    except Exception as e:
        logging.error("Errore durante l'aggiunta dell'utente: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500
   #GET     
@app.route('/get_users', methods=['GET'])
def get_users():
    logging.info('GET /get_users')
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id':user.id,
            'name': user.name,
            'surname': user.surname
        }
        user_list.append(user_data)
    logging.info('User list retrieved')
    return jsonify(user_list), 200       

@app.route('/get_id/<int:id>', methods=['GET'])
def get_id(id):
    logging.info(f'GET /get_id/{id}')
    user = User.query.get(id)
    if user:
        logging.info(f'User with id {id} found')
        return '', 200
    else:
        logging.error(f'User with id {id} not found')
        return '', 404




#DELETE
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    logging.info(f'DELETE /delete_user/{id}')
    user = User.query.get(id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        logging.info(f'User with id {id} deleted')
        return jsonify({"message": "Utente eliminato con successo"}), 200
    else:
        logging.error(f'User with id {id} not found')
        return jsonify({"error": "Utente non trovato"}), 404


# PUT
@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    logging.info(f'PUT /update_user/{id}')
    data = request.get_json()
    if 'name' not in data or 'surname' not in data:
        logging.error("Campi name o surname vuoti")
        return jsonify({"error": "Campi name o surname vuoti"})
    try:
        user = User.query.get(id)
        if user is not None:
            user.name = data['name']
            user.surname = data['surname']
            db.session.commit()
            logging.info(f'User with id {id} updated')
            return jsonify({"message": "Utente aggiornato con successo"}), 200
        else:
            logging.error(f'User with id {id} not found')
            return jsonify({"error": "Utente non trovato"}), 404
    except Exception as e:
        logging.error(f'Error updating user with id {id}: {str(e)}')
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
