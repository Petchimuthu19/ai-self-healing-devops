FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .

COPY templates ./templates

EXPOSE 5000

CMD ["python3", "app.py"]
