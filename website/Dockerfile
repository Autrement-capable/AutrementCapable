FROM node:14

WORKDIR /app

COPY package*.json ./

RUN yarn install

COPY . .

EXPOSE 8081

CMD [ "yarn", "serve", "--port", "8081"]