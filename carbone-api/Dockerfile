FROM bcgovimages/alpine-node-libreoffice
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app
RUN mkdir -p /home/node/app/report-downloads
RUN mkdir -p /home/node/app/template-uploads
WORKDIR /home/node/app
COPY package*.json ./
COPY earning-statment.odt ./template-uploads/
RUN chown -R node:node package*.json
USER node
RUN npm install

COPY --chown=node:node . .
EXPOSE 3000
CMD ["node", "app.js"]