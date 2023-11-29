# Usa un'immagine di Python ufficiale come base
FROM python:3.8

# Imposta il work directory nell'immagine
WORKDIR /app/notifiche

# Copia i file necessari nell'immagine

COPY . /app
# Installa le dipendenze
RUN pip install --no-cache-dir -r /app/notifiche/requirements.txt

# Comando di avvio dell'applicazione
CMD ["python", "notifiche.py"]
