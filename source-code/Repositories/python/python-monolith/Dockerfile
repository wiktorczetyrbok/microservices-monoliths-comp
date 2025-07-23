FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y unzip

RUN pip install gunicorn

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN unzip data/geo.zip -d data
RUN unzip data/hotels.zip -d data
RUN unzip data/inventory.zip -d data

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "src.main:app"]