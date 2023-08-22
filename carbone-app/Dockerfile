FROM node:13.12.0-alpine
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

WORKDIR /home/node/app
COPY package*.json ./
COPY src ./
USER node

RUN npm install

COPY --chown=node:node . .
EXPOSE 3006

ENV NODE_ENV=production GENERATE_SOURCEMAP=false DISABLE_ESLINT_PLUGIN=true

RUN npm run build
CMD ["npm", "start"]

