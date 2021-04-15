# FROM node:lts-alpine
FROM node:7.7.2-alpine 
WORKDIR /usr/app 
COPY package.json . 
RUN npm install --quiet 
COPY . .

# install simple http server for serving static content
# RUN apk add --no-cache --virtual .gyp \
#         python \
#         make \
#         g++ \
#     && npm install \
#         -g http-server \
#     && apk del .gyp
#RUN npm install -g http-server

# RUN apk add --no-cache --virtual .gyp \
#         python \
#         make \
#         g++ \
#     # && npm install \
#         # [ your npm dependencies here ] \
#     && apk del .gyp

# make the 'app' folder the current working directory
#WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
#COPY package*.json ./

# install project dependencies
#RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
#COPY . .

# build app for production with minification
# RUN npm run build

# EXPOSE 8080
# CMD [ "http-server", "dist" ]
#CMD ["npm", "run","serve"]