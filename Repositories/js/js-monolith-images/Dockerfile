FROM node:20-slim

ENV NODE_ENV=production

WORKDIR /app

RUN apt-get update && apt-get install -y unzip \
    && rm -rf /var/lib/apt/lists/*

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 8080

CMD ["node", "main.js"]