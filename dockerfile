# Image chính thức của Python
FROM python:3.13-slim

# Tạo thư mục làm việc
WORKDIR /app

# Copy file dependency và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app

EXPOSE 8000

# Chạy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
