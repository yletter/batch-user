FROM python:3.11-slim

WORKDIR /app

COPY init_db.py .

RUN pip install mysql-connector-python

CMD ["python", "init_db.py"]
