FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Install serve to run the production build
RUN npm install -g serve

# Expose port (Render will use PORT env variable)
EXPOSE 5173

# Start production server
CMD sh -c "serve -s dist -l ${PORT:-5173}"
