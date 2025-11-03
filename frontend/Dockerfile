### Multi-stage build for frontend (Vite + React) -> nginx
FROM node:18-alpine AS builder
WORKDIR /app/frontend

# Install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --silent || npm install --silent

# Copy source and build
COPY frontend/ ./
RUN npm run build

### Production image: nginx serving built assets
FROM nginx:stable-alpine
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

# SPA fallback: route all to index.html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
