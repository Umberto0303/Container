from flask import Flask, request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://mysql:mysql@dbprestiti/mysql'

db = SQLAlchemy(app)



class Prestito(db.Model):
    __tablename__ = 'prestiti'
    id = db.Column(db.Integer, primary_key=True)
    IdCliente = db.Column(db.Integer)
    IdLibro = db.Column(db.Integer)

    def json(self):
        return {'id': self.id, 'IdCliente': self.IdCliente, 'IdLibro': self.IdLibro}
with app.app_context():
     db.create_all()

@app.route('/PROVA', methods=['POST'])
def add_loan():
    try:
        data = request.get_json()

        if 'IdCliente' not in data or 'IdLibro' not in data:
            return jsonify({"error": "Both 'IdCliente' and 'IdLibro' fields are required."})

        new_loan = Prestito(IdCliente=data['IdCliente'], IdLibro=data['IdLibro'])
        db.session.add(new_loan)
        db.session.commit()
        return jsonify({"message": "Prestito aggiunto"}), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Stampa l'errore nel log
        return jsonify({"error": str(e)}), 500

@app.route('/get_loans', methods=['GET'])
def get_loans():
    # Esegui una query per ottenere tutti i prestiti dal database
    loans = Prestito.query.all()

    # Crea una lista di dizionari contenenti le informazioni dei prestiti
    loan_list = []
    for loan in loans:
        loan_data = {
            'id': loan.id,
            'IdCliente': loan.IdCliente,
            'IdLibro': loan.IdLibro,
        }
        loan_list.append(loan_data)

    # Restituisci la lista di prestiti come risposta JSON
    return jsonify(loan_list), 200

@app.route('/delete_loan/<int:id>', methods=['DELETE'])
def delete_loan(id):
    try:
        # Trova il prestito nel database
        loan = Prestito.query.get(id)

        # Se il prestito non esiste, restituisci un errore
        if loan is None:
            return jsonify({"error": "Prestito non trovato"}), 404

        # Rimuovi il prestito dal database
        db.session.delete(loan)
        db.session.commit()

        # Restituisci un messaggio di successo
        return jsonify({"message": "Prestito rimosso"}), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Stampa l'errore nel log
        return jsonify({"error": str(e)}), 500

@app.route('/update_loan/<int:id>', methods=['PUT'])
def update_loan(id):
    try:
        # Trova il prestito nel database
        loan = Prestito.query.get(id)

        # Se il prestito non esiste, restituisci un errore
        if loan is None:
            return jsonify({"error": "Prestito non trovato"}), 404

        # Ottieni i dati dal corpo della richiesta
        data = request.get_json()

        # Aggiorna i campi del prestito
        if 'IdCliente' in data:
            loan.IdCliente = data['IdCliente']
        if 'IdLibro' in data:
            loan.IdLibro = data['IdLibro']

        # Salva le modifiche nel database
        db.session.commit()

        # Restituisci un messaggio di successo
        return jsonify({"message": "Prestito aggiornato"}), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Stampa l'errore nel log
        return jsonify({"error": str(e)}), 500

@app.route('/add', methods=['POST'])
def aggiungi_prestito_verificato():
    
    data = request.get_json()
    Id_Cliente = data['IdCliente']
    Id_Libro = data['IdLibro']
        
        
    response = requests.get(f'http://utenti:4000/get_id/{Id_Cliente}')
    if response.status_code != 200:
        return jsonify({'message': 'Cliente non trovato'}), 404

    response = requests.get(f'http://libri:5000/get_books/{Id_Libro}')
    if response.status_code != 200:
        return jsonify({'message': 'Libro non trovato'}), 404

    try:
        new_loan = Prestito(IdCliente=data['IdCliente'], IdLibro=data['IdLibro'])
        db.session.add(new_loan)
        db.session.commit()
        return jsonify({'message': 'Prestito aggiunto'}), 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Log the error
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
 