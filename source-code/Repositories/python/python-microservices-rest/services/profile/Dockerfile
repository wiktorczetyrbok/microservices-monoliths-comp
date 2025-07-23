FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /profile

RUN apt-get update && apt-get install -y unzip

COPY requirements.txt .

RUN pip install gunicorn

RUN pip install --no-cache-dir -r requirements.txt

COPY services/profile/data/hotels.zip .

RUN unzip hotels.zip -d data

COPY services/profile .

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "main:app"]