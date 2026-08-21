FROM node:18-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --production=false

COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app

ENV NODE_ENV=production
ENV DATA_DIR=/app/data

RUN apk add --no-cache iputils

COPY package.json package-lock.json ./
RUN npm ci --production

COPY --from=build /app/dist ./dist
COPY --from=build /app/server ./server
COPY --from=build /app/db ./db
COPY --from=build /app/src ./src

EXPOSE 3001
CMD ["node", "server/server.js"]
