FROM python:3.12-slim@sha256:4b8e6b3306763dcad4d1961873e578e0dccab2c39c0b8abe25c5a614e92e2fc8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
