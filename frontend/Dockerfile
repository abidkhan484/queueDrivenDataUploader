FROM node:20

WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .
RUN yarn build
EXPOSE 80

ENV HOST=0.0.0.0
ENV PORT=80

# Run the React app
CMD ["yarn", "start"]
