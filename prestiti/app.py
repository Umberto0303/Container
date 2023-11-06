from flask import Flask, request, jsonify
#from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)
db=SQLAlchemy(app)


###############LIBRI

POSTGRES_USER= 'postgres'
POSTGRES_PASSWORD= 'postgres'
POSTGRES_DB= 'db_postgresLIBRI'
POSTGRES_HOST= 'db_libri'
POSTGRES_PORT='13002'
SQLALCHEMY_DATABASE_URI_USERS=f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

##########UTENTI

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DB = 'db_postgres'
POSTGRES_HOST = 'dbutenti'
POSTGRES_PORT = '13001'
SQLALCHEMY_DATABASE_URI_USERS = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

############PRESTITI

MYSQL_ROOT_PASSWORD = 'mysql'
MYSQL_USER = 'mysql'
MYSQL_PASSWORD = 'mysql'
MYSQL_DATABASE = 'mysql'
MYSQL_HOST = 'dbprestiti'
MYSQL_PORT = '13000'
SQLALCHEMY_DATABASE_URI_PRESTITI = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'




# Configura la connessione al database MySQL
#app.config['MYSQL_HOST'] = 'dbprestiti'  # Nome del servizio Docker Compose del database MySQL
#app.config['MYSQL_USER'] = 'mysql'
#app.config['MYSQL_PASSWORD'] = 'mysql'
#app.config['MYSQL_DB'] = 'mysql'
mysql = SQLAlchemy(app)

# API per ottenere la lista dei prestiti
@app.route('/prestiti', methods=['GET'])
def get_prestiti():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM prestiti')
    prestiti = cur.fetchall()
    cur.close()
    return jsonify(prestiti)

# API per aggiungere un prestito
@app.route('/prestiti', methods=['POST'])
def add_prestito():
    data = request.get_json()
    nome = data['nome']
    libro = data['libro']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO prestiti (nome, libro) VALUES (%s, %s)', (nome, libro))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Prestito aggiunto con successo'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
