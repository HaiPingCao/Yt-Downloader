# Image chính thức của Python
FROM python:3.14.5-slim

# Tạo thư mục làm việc
WORKDIR /app

# Copy file dependency và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app

EXPOSE 8000

# Chạy
CMD ["uvicorn", "run_server:app", "--host", "0.0.0.0", "--port", "8000"]
