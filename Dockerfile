FROM python:3-alpine

RUN pip install flask gunicorn  Flask-And-Redis

COPY app.py /app.py

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
