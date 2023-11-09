from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask import abort
import mysql.connector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mysql:mysql@dbprestiti:13003/mysql'

db = SQLAlchemy(app)

class Prestito(db.Model):
    __tablename__ = 'prestiti'
    id = db.Column(db.Integer, primary_key=True)
    IdCliente = db.Column(db.Integer)
    IdLibro = db.Column(db.Integer)

    def json(self):
        return {'id': self.id, 'IdCliente': self.IdCliente, 'IdLibro': self.IdLibro}
     

def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="dbprestiti",  # Docker Compose esegue i servizi in rete locale
            user="mysql",  # Nome utente definito nel tuo servizio dbprestiti
            passwd="mysql",  # Password definita nel tuo servizio dbprestiti
            database="mysql"  # Nome del database definito nel tuo servizio dbprestiti
        )
        print("Connessione al database MySQL riuscita")
    except Exception as e:
        print(f"L'errore '{e}' è accaduto")
    return connection
# Funzione per verificare l'esistenza di un cliente

@app.route('/add', methods=['POST'])
def aggiungi_prestito_verificato():
    try:
        conn = create_db_connection()
        cursor = conn.cursor() 

        data = request.get_json()
        IdCliente = data['IdCliente']
        IdLibro = data['IdLibro']
        
        if not controllo_cliente(IdCliente):
            return jsonify({'error': 'Cliente non valido'}), 401
        if not controllo_libro(IdLibro):
            return jsonify({'error': 'Libro non valido'}), 401
        insert_query = "INSERT INTO prestiti (IdCliente, IdLibro) VALUES (%s, %s)"
        values = (IdCliente, IdLibro)
        cursor.execute(insert_query, values)

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Prestito aggiunto con successo'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 401

def controllo_cliente(IdCliente):
    try:
        response = request.get(f'http://localhost:4000/get_id/{IdCliente}')
        if response.status_code == 200:
            data = response.json()
            return data['id']
    except Exception as e:
     print(f"Errore durante il controllo del cliente: {str(e)}")
    return False

# Funzione per verificare l'esistenza di un libro
def controllo_libro(IdLibro):
    try:
        response = request.get(f'http://localhost:5000/get_books/{IdLibro}')
        if response.status_code == 200:
            data = response.json()
            return data['id']
    except Exception as e:
        return False
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
 