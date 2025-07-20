FROM python:3.11-slim

WORKDIR /app

# Copy everything first
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Railway uses $PORT environment variable
ENV PORT=8000
EXPOSE $PORT

# Use Railway's port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 