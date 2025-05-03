FROM python:3.12-slim
WORKDIR /app
COPY . /app
ENV PYTHONPATH=/app
RUN pip install --no-cache-dir fastapi uvicorn httpx pydantic pytest pytest-asyncio
CMD ["uvicorn", "app.services.data.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
