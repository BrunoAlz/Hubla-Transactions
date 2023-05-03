FROM node:19.9.0

WORKDIR /frontend

COPY . .

RUN npm install

EXPOSE 3000

# ENTRYPOINT ["tail", "-f", "/dev/null"]
CMD ["npm", "run", "dev"]
