FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /search

COPY requirements.txt .

RUN pip install gunicorn

RUN pip install --no-cache-dir -r requirements.txt

COPY services/search .

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "main:app"]