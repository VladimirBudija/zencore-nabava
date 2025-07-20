FROM python:3.11-slim

WORKDIR /app

# Copy backend directory
COPY backend/ .

# Copy start script and version
COPY start.py .
COPY VERSION.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Railway uses $PORT environment variable
ENV PORT=8000
EXPOSE $PORT

# Use Python start script
CMD ["python", "start.py"] 