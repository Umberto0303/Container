import pika

# Connessione a RabbitMQ
try:
    # Connessione a RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Dichiarazione della coda 'notifiche'
    channel.queue_declare(queue='notifiche')

    # Definizione della funzione di callback che verrà chiamata quando un messaggio viene ricevuto
    def callback(ch, method, properties, body):
        print(f"Ricevuto messaggio di notifica: {body}")

    # Avvio del consumatore
    channel.basic_consume(queue='notifiche', on_message_callback=callback, auto_ack=True)

    print('In attesa di messaggi di notifica. Per uscire premi CTRL+C')
    channel.start_consuming()  # Chiamata bloccante, attende i messaggi. Interrompi manualmente con CTRL+C
except pika.exceptions.AMQPConnectionError as e:
    print(f"Errore di connessione a RabbitMQ: {str(e)}")