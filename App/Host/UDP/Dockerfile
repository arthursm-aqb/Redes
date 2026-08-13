FROM python:latest

WORKDIR /app

RUN pip install cryptography

COPY . .

CMD ["python", "servidorUDP.py"]
