# Use python image
FROM python:3.14.5-slim
# Create app directory
WORKDIR /app
# Copy file dependency and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src /app
# Expose port
EXPOSE 8000
# Set environment variables
ENV WS_URL="/ws/music"
# Run
CMD ["uvicorn", "run_server:app", "--host", "0.0.0.0", "--port", "8000"]
