FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /gateway

COPY requirements.txt .

RUN pip install gunicorn

RUN pip install --no-cache-dir -r requirements.txt

COPY services/gateway .

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "main:app"]