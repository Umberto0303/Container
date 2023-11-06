from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 

#################################UTENTI#############################
app = Flask(__name__)

# Configura la connessione al database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@dbutenti/db_postgres'

# DB
db=SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(50), unique=True)
    surname = db.Column(db.String(50)) 
    def json(self):
         return {'Id':self.id,'name':self.name,'surname':self.surname}
with app.app_context():
     db.create_all()

#POST
@app.route('/add_user', methods=['POST'])
def add_user():
        data = request.get_json()
        
        if 'name'not in data or 'surname' not in data:   # Assicurati che entrambi i campi siano presenti           
            return jsonify({"error": "Both 'name' and 'surname' fields are required."})
        try:
            new_users=User(name=data['name'],surname=data['surname'])
            db.session.add(new_users)
            db.session.commit()
            return jsonify({"message": "utente aggiunto"}),200

        except Exception as e:
            return jsonify({"message": str(e)}),500

   #GET     
@app.route('/get_users', methods=['GET'])
def get_users():
    # Esegui una query per ottenere tutti gli utenti dal database
    users = User.query.all()

    # Creare una lista di dizionari contenenti i nomi e i cognomi degli utenti
    user_list = []
    for user in users:
        user_data = {
            'id':user.id,
            'name': user.name,
            'surname': user.surname
        }
        user_list.append(user_data)

    # Restituisci la lista di utenti come risposta JSON
    return jsonify(user_list), 200        

#DELETE
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    # Cerca l'utente nel database
    user = User.query.get(id)

    if user is not None:
        # Elimina l'utente dal database
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Utente eliminato con successo"}), 200
    else:
        return jsonify({"error": "Utente non trovato"}), 404


#POST 
# PUT
@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()

    if 'name' not in data or 'surname' not in data:
        return jsonify({"error": "error name not found"})

    try:
        user = User.query.get(id)

        if user is not None:
            user.name = data['name']
            user.surname = data['surname']
            db.session.commit()
            return jsonify({"message": "Utente aggiornato con successo"}), 200
        else:
            return jsonify({"error": "Utente non trovato"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
