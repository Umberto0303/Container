from flask import Flask, request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import requests
import pika
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://mysql:mysql@dbprestiti/mysql'

db = SQLAlchemy(app)


class Prestito(db.Model):
    __tablename__ = 'prestiti'
    id = db.Column(db.Integer, primary_key=True)
    IdCliente = db.Column(db.Integer)
    IdLibro = db.Column(db.Integer)
    disponibile = db.Column(db.Boolean, default=False)  # Aggiungi il campo 'disponibile'
    def json(self):
        return {'id': self.id, 'IdCliente': self.IdCliente, 'IdLibro': self.IdLibro, 'disponibile': self.disponibile}
with app.app_context():
     db.create_all()

# Connessione a RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))  # Usa l'hostname del servizio RabbitMQ nel tuo file docker-compose
channel = connection.channel()

# Creazione di una coda 'notifiche'
channel.queue_declare(queue='notifiche')


@app.route('/get_loans', methods=['GET'])
def get_loans():
    logging.info('GET /get_loans')
    loans = Prestito.query.all()
    loan_list = []
    for loan in loans:
        loan_data = {
            'id': loan.id,
            'IdCliente': loan.IdCliente,
            'IdLibro': loan.IdLibro,
        }
        loan_list.append(loan_data)
        logging.info(f'Loan data: {loan_data}')
    return jsonify(loan_list), 200

@app.route('/update_loan/<int:id>', methods=['PUT'])
def update_loan(id):
    logging.info(f'PUT /update_loan/{id}')
    try:
        loan = Prestito.query.get(id)
        if loan is None:
            return jsonify({"error": "Prestito non trovato"}), 404
        data = request.get_json()
        if 'IdCliente' in data:
            loan.IdCliente = data['IdCliente']
        if 'IdLibro' in data:
            loan.IdLibro = data['IdLibro']
        if 'disponibile' in data:
            loan.disponibile = data['disponibile']
            if loan.disponibile:
                notification_message = f'Il prestito {id} è ora disponibile'
                channel.basic_publish(exchange='', routing_key='notifiche', body=notification_message)
                print("Messaggio di notifica inviato")
        db.session.commit()
        return jsonify({"message": "Prestito aggiornato"}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            if connection and connection.is_open:
                connection.close()
                print("Connessione RabbitMQ chiusa con successo")
        except Exception as e:
            print(f"Errore durante la chiusura di RabbitMQ: {str(e)}")

@app.route('/add', methods=['POST'])
def aggiungi_prestito_verificato():
    logging.info('POST /add')
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
        new_loan = Prestito(IdCliente=data['IdCliente'], IdLibro=data['IdLibro'],disponibile=False)
        db.session.add(new_loan)
        db.session.commit()
        return jsonify({'message': 'Prestito aggiunto'}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

@app.route('/get_loan/<int:id>', methods=['GET'])
def get_loan(id):
    logging.info(f'GET /get_loan/{id}')
    try:
        loan = Prestito.query.get(id)
        if loan is None:
            return jsonify({"error": "Prestito non trovato"}), 404
        loan_data = {
            'id': loan.id,
            'IdCliente': loan.IdCliente,
            'IdLibro': loan.IdLibro,
        }
        return jsonify(loan_data), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete_loan/<int:id>', methods=['DELETE'])
def delete_loan(id):
    logging.info(f'DELETE /delete_loan/{id}')
    try:
        loan = Prestito.query.get(id)
        if loan is None:
            return jsonify({"error": "Prestito non trovato"}), 404
        db.session.delete(loan)
        db.session.commit()
        return jsonify({"message": "Prestito eliminato"}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
 