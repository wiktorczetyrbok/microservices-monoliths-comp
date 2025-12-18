FROM node:20-slim

ENV NODE_ENV=production

WORKDIR /app

# unzip like in python image
RUN apt-get update && apt-get install -y unzip \
    && rm -rf /var/lib/apt/lists/*

# install deps first (better cache)
COPY package*.json ./
RUN npm install --production

# copy rest of app
COPY . .

RUN unzip -o data/geo.zip -d data

EXPOSE 8080

CMD ["node", "src/main.js"]