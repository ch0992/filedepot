# docker/data/Dockerfile
# Data 서비스용 Dockerfile (placeholder)
FROM python:3.11-slim
WORKDIR /app
COPY ../../app/data/ .
RUN pip install fastapi uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
