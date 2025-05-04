FROM python:3.12-slim
WORKDIR /app

# requirements.txt만 먼저 복사 (캐시 활용)
COPY /requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y curl \
    && pip install --no-cache-dir -r /app/requirements.txt

# 전체 소스 복사 (이 아래가 자주 invalidate됨)
COPY app /app/app
ENV PYTHONPATH=/app/app

CMD ["uvicorn", "app.services.file.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
