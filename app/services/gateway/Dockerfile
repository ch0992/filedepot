FROM python:3.12-slim
WORKDIR /app

# uv 설치
RUN pip install --no-cache-dir uv

# requirements.txt만 먼저 복사 (캐시 활용)
COPY /requirements.txt /app/requirements.txt
RUN uv pip install --system -r /app/requirements.txt

# 전체 소스 복사 (이 아래가 자주 invalidate됨)
COPY . /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.services.gateway.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
