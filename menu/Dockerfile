# FROM python:3.8-slim
# WORKDIR /app/menu
# COPY menu /app/menu
# WORKDIR /app/menu
# RUN pip install --no-cache-dir -r requirements.txt
# # Expose port 8000 for the FastAPI server
# EXPOSE 8000
# # Command to run the FastAPI server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.8-slim
WORKDIR /app/menu
COPY . /app/menu
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI server
EXPOSE 8000
# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
