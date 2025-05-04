FROM python:3.12-slim
WORKDIR /app
COPY app /app/app
COPY app/services/file/requirements.txt /app/requirements.txt
ENV PYTHONPATH=/app/app
RUN apt-get update && apt-get install -y curl \
    && pip install --no-cache-dir -r /app/requirements.txt
CMD ["uvicorn", "app.services.file.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
