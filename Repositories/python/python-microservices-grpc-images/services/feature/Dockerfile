FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /feature

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt



COPY services/feature .

CMD ["python", "main.py"]