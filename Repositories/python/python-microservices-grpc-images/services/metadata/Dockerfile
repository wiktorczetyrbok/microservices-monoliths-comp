FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /metadata

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/metadata .

CMD ["python", "main.py"]