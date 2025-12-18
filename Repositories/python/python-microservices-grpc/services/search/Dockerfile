FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /search

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/search .

CMD ["python", "main.py"]