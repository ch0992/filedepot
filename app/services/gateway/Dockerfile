FROM python:3.12-slim
WORKDIR /app
COPY . /app
ENV PYTHONPATH=/app
RUN apt-get update && apt-get install -y curl \
    && pip install --no-cache-dir fastapi uvicorn httpx pydantic pytest pytest-asyncio
CMD ["uvicorn", "app.services.gateway.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
