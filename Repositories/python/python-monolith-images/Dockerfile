FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install gunicorn

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "src.main:app"]