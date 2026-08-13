FROM python:latest

WORKDIR /app

RUN pip install psutil cryptography

COPY . .

EXPOSE 6000

CMD ["python", "cliente.py"]
