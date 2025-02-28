FROM python:latest

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY app.py /app

EXPOSE 5000

CMD ["python3", "app.py"]