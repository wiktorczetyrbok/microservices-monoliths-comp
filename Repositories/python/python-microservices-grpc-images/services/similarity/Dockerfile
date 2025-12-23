FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /similarity

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/similarity .

CMD ["python", "main.py"]