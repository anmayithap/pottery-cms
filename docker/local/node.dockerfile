FROM node:22-alpine

ENV PROJECT_DIR /opt/pottery

WORKDIR ${PROJECT_DIR}

COPY package.json ${PROJECT_DIR}

RUN npm install && npm cache clean --force

ENV PATH ${PROJECT_DIR}/node_modules/.bin/:$PATH
