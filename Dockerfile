FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY server.py .
COPY api/ ./api/
COPY static/ ./static/
COPY templates/ ./templates/
COPY .env ./.env

# Create necessary directories
RUN mkdir -p /app/temp_uploads

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5)"

# Run the FastAPI server
CMD ["python", "server.py"]
