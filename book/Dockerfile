# Usa l'immagine di base di Python
FROM python:3.8-slim-buster

# Imposta la directory di lavoro nell'immagine
WORKDIR /app

 # Copia il tuo codice sorgente nell'immagine
COPY requirements.txt .
COPY app.py .
# Installa le dipendenze Python
RUN pip install -r requirements.txt


# Espone la porta su cui Flask ascolterà
EXPOSE 5000

ENV FLASK_APP=app.py

# Avvia l'applicazione Flask
CMD ["flask","run","--host=0.0.0.0","--port=5000"]
