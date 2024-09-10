FROM python:3.9
WORKDIR /app/calendar
COPY calendar /app/calendar
WORKDIR /app/calendar
RUN pip install --no-cache-dir -r requirements.txt
# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

