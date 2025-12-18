FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /geo

RUN apt-get update && apt-get install -y unzip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/geo/data/geo.zip .

RUN unzip -o geo.zip -d data

COPY services/geo .

CMD ["python", "main.py"]