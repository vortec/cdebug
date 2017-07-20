FROM python:3-alpine

RUN pip install flask gunicorn

COPY app.py /app.py

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
