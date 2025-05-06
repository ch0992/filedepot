# Filedepot Kubernetes Porting Guide

본 문서는 filedepot 프로젝트를 쿠버네티스(Kubernetes) 환경(stage/production)으로 포팅하기 위한 실질적 가이드입니다. 개발(local) 환경과의 차이, 환경변수 관리, 서비스별 분기, 실서비스/모의(mock) 연동 방식, 배포 체크리스트 등을 모두 포함합니다.

---

## 1. 환경 및 구조 개요

- **서비스 구조**: gateway, file, data, log 등 각 서비스별로 컨테이너화 및 별도 Pod로 배포
- **환경 구분**: development(local), stage, production
- **환경변수 관리**: 개발은 .env 파일, K8s는 ConfigMap/Secret으로 환경변수 주입
- **코드 구조**: 모든 환경설정은 `app/core/config.py`의 `Settings` 클래스에서 통합 관리

---

## 2. 반드시 변경/설정해야 하는 환경변수

| 환경변수           | 개발(localhost) 예시        | K8s/Stage/Prod 예시      | 설명                      |
|--------------------|----------------------------|--------------------------|---------------------------|
| ENV                | development                | stage, production        | 환경 구분                  |
| FILE_SERVICE_URL   | http://localhost:8001      | http://file:8001         | 파일 서비스 엔드포인트     |
| DATA_SERVICE_URL   | http://localhost:8002      | http://data:8002         | 데이터 서비스 엔드포인트   |
| LOG_SERVICE_URL    | http://localhost:8003      | http://log:8003          | 로그 서비스 엔드포인트     |
| SENTRY_DSN         | (빈 값/미설정)             | 실제 DSN 값              | Sentry 연동 주소           |
| USE_SENTRY         | false                      | true                     | Sentry 연동 활성화 여부    |
| OTEL_EXPORTER      | stdout                     | jaeger/tempo/otlp 등     | OTEL 익스포터 종류         |
| KAFKA_BROKER       | localhost:9092             | kafka:9092               | Kafka 브로커 주소          |
| MINIO_ENDPOINT     | http://localhost:9000      | http://minio:9000        | MinIO 엔드포인트           |
| LOG_LEVEL          | DEBUG/INFO                 | INFO/WARN                | 로그 레벨                  |
| AUTH_MODE          | local                      | remote/local             | 인증 모드                  |
| DB_URL             | sqlite:///./test.db        | postgresql://...         | DB 연결 문자열             |
| JWT_SECRET         | (직접 입력/테스트용)        | (Secret에서 주입)        | JWT 서명 키                |

---

## 3. 코드 내 환경별 분기 패턴

- 모든 서비스(main.py, 클라이언트 등)는 반드시 `from app.core.config import settings`로 Settings 인스턴스를 사용
- ENV 값에 따라 실서비스/모의(mock) 연동 분기

```python
if settings.ENV in ["production", "stage"]:
    # 실서비스 연동(외부 주소, Sentry, OTEL, Kafka, MinIO 등)
else:
    # 개발/테스트(mock, dummy, localhost 등)
```

### Kafka/MinIO 예시
```python
if settings.ENV in ["production", "stage"]:
    minio_client = MinioProdClient()
else:
    minio_client = MinioMemoryClient()
```

---

## 4. 환경변수 주입 방법

- **개발 환경**: 프로젝트 루트에 `.env` 파일 작성(예시: `.env.example` 참고)
- **쿠버네티스 환경**: ConfigMap(일반 설정), Secret(민감 정보)로 환경변수 주입
    - 예시: `kubectl create configmap filedepot-config --from-env-file=.env.stage`
    - 예시: `kubectl create secret generic filedepot-secret --from-literal=JWT_SECRET=...`
- **.env 파일은 개발 환경에서만 사용**, K8s에서는 절대 사용하지 않음

---

## 5. 포팅 체크리스트

- [ ] 모든 서비스(main.py 등)에서 Settings 기반 ENV 분기 적용
- [ ] Kafka/MinIO 등 외부 연동 코드에서 mock/dummy 분기 구현
- [ ] 환경변수 미설정 시 안전한 기본값 적용 및 예외 메시지 명확화
- [ ] .env 파일 의존성 제거(쿠버네티스 환경)
- [ ] README/문서에 환경변수 및 포팅 방법 명시

---

## 6. 참고/팁

- Sentry, OTEL 등 외부 연동은 DSN/Exporter 값이 없으면 자동 fallback(미연동) 처리
- Swagger/OpenAPI 문서, 라우터 등록 등은 gateway에서 통합 관리
- 로그/예외처리 등도 환경별로 적절히 분기
- 실제 배포 전, K8s 환경에서 모든 환경변수와 Secret이 올바르게 주입되었는지 반드시 확인

---

## 7. 예시: .env 파일 템플릿

```env
ENV=stage
FILE_SERVICE_URL=http://file:8001
DATA_SERVICE_URL=http://data:8002
LOG_SERVICE_URL=http://log:8003
SENTRY_DSN=your_sentry_dsn
USE_SENTRY=true
OTEL_EXPORTER=jaeger
KAFKA_BROKER=kafka:9092
MINIO_ENDPOINT=http://minio:9000
LOG_LEVEL=INFO
AUTH_MODE=remote
DB_URL=postgresql://user:password@db:5432/filedepot
JWT_SECRET=your_jwt_secret
```

---

이 가이드에 따라 환경별 설정 및 코드를 점검하면 filedepot 프로젝트를 안전하게 쿠버네티스 환경으로 포팅할 수 있습니다.

추가 문의/상세 예시가 필요하면 언제든 문의하세요.
