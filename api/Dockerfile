FROM node:14-alpine

WORKDIR /home/node/app

COPY . /home/node/app/

RUN npm install

EXPOSE 8080

CMD ["node","serveur.js"]