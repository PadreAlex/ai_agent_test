FROM node:22.14-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm i && npm i typescript
COPY . .
RUN npm run build

FROM node:22.14-alpine
WORKDIR /app
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/dist ./dist
RUN npm i --omit=dev
CMD ["node", "dist/main.js"]