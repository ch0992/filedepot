FROM python:3.12-slim
WORKDIR /app
COPY . /app
ENV PYTHONPATH=/app

# uv 설치
RUN pip install --no-cache-dir uv

# requirements.txt 복사 및 uv로 패키지 설치
COPY app/services/gateway/requirements.txt /app/requirements.txt
RUN uv pip install --system -r /app/requirements.txt

CMD ["uvicorn", "app.services.gateway.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
