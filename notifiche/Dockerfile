FROM python:3.6-slim-buster

WORKDIR /notifiche

COPY notifiche/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY notifiche/notifiche.py ./

CMD ["python3", "notifiche.py"]