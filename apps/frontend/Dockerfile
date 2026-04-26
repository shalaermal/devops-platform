# Faza 1 - Build
# Marrim Node.js si bazë
FROM node:20-alpine AS builder

# Krijojmë folderin e punës brenda containerit
WORKDIR /app

# Kopjojmë package.json fillimisht (për cache)
COPY package*.json ./

# Instalojmë dependencies
RUN npm install

# Kopjojmë gjithë kodin
COPY . .

# Buildojmë React app për produksion
RUN npm run build

# Faza 2 - Production
# Nginx shërben faqen - është i lehtë dhe i shpejtë
FROM nginx:alpine

# Kopjojmë buildin nga faza 1 te Nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Nginx dëgjon në portin 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]