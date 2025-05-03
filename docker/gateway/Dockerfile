# docker/gateway/Dockerfile
# Gateway 서비스용 Dockerfile (placeholder)
FROM python:3.11-slim
WORKDIR /app
COPY app /app
COPY docker/gateway/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "services.gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
