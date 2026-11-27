services:

  backend:
    build: .
    container_name: third-eye-backend
    ports:
      - "8000:8000"
    environment:
      GEMINI_API_KEY: ${GEMINI_API_KEY:-}
    restart: unless-stopped

  frontend:
    image: nginx:alpine
    container_name: third-eye-frontend
    ports:
      - "8080:80"
    volumes:
      - ./frontline:/usr/share/nginx/html:ro
    restart: unless-stopped