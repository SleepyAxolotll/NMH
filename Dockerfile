FROM python:3.8-slim
WORKDIR /app
COPY menu /app/menu
WORKDIR /app/menu
COPY requirements.txt /app/menu/
RUN pip install --no-cache-dir -r requirements.txt
