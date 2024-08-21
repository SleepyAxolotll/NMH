FROM python:3.8-slim
WORKDIR /app/menu
COPY menu /app/menu
WORKDIR /app/menu
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
