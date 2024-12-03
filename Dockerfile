# Dockerfile
FROM python:3.11-slim

# Устанавливаем зависимости
WORKDIR /app
COPY . /app

# Запускаем main.py
CMD ["python", "main.py"]
