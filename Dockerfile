FROM python:3.11-slim

WORKDIR /app

# Copy backend directory
COPY backend/ .

# Copy start script
COPY start.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Railway uses $PORT environment variable
ENV PORT=8000
EXPOSE $PORT

# Use Python start script
CMD ["python", "start.py"] 