FROM python:3-alpine

RUN pip install flask gunicorn

COPY app.py /app.py

PORT 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
