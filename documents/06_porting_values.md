# 06_porting_values: Kubernetes 포팅 시 반드시 변경/설정해야 하는 값 정리

이 문서는 filedepot 프로젝트를 쿠버네티스(Kubernetes) 환경(stage/production)으로 포팅할 때 반드시 변경·설정해야 할 모든 환경변수와 주요 값을 한눈에 보기 쉽게 나열하고, 각 항목의 의미와 사용처를 설명합니다.

---

## 1. 환경 구분 및 서비스 엔드포인트

- **ENV**
  - 환경 구분 (development, stage, production 등)
  - 개발 환경: `development`, 운영/스테이지: `stage` 또는 `production`
- **FILE_SERVICE_URL**
  - 파일 서비스 엔드포인트 주소
  - 개발: `http://localhost:8001`, K8s: `http://file:8001`
- **DATA_SERVICE_URL**
  - 데이터 서비스 엔드포인트 주소
  - 개발: `http://localhost:8002`, K8s: `http://data:8002`
- **LOG_SERVICE_URL**
  - 로그 서비스 엔드포인트 주소
  - 개발: `http://localhost:8003`, K8s: `http://log:8003`

---

## 2. 외부 연동(Sentry, OTEL 등)

- **SENTRY_DSN**
  - Sentry 연동 주소(DSN)
  - 운영/스테이지 환경에서 실제 DSN 값 사용, 개발 환경에서는 빈 값 또는 미설정
- **USE_SENTRY**
  - Sentry 연동 활성화 여부 (`true`/`false`)
  - 운영/스테이지 환경에서만 `true` 권장
- **OTEL_EXPORTER**
  - OpenTelemetry 익스포터 종류(`stdout`, `jaeger`, `tempo`, `otlp` 등)
  - 개발 환경은 `stdout`, 운영은 실제 익스포터 지정

---

## 3. Kafka, MinIO 등 외부 서비스

- **KAFKA_BROKER**
  - Kafka 브로커 주소
  - 개발: `localhost:9092`, K8s: `kafka:9092`
- **MINIO_ENDPOINT**
  - MinIO/S3 엔드포인트 주소
  - 개발: `http://localhost:9000`, K8s: `http://minio:9000`

---

## 4. 인증, 로깅, 기타

- **AUTH_MODE**
  - 인증 모드(`local`, `remote`)
  - 개발 환경은 `local`, 운영은 필요에 따라 `remote` 또는 `local`
- **LOG_LEVEL**
  - 로그 레벨(`DEBUG`, `INFO`, `WARN` 등)
  - 운영 환경은 `INFO` 이상 권장

---

## 5. DB 및 시크릿

- **DB_URL**
  - DB 연결 문자열
  - 개발: `sqlite:///./test.db`, 운영: `postgresql://...` 등 실 DB 주소
- **JWT_SECRET**
  - JWT 서명 키(반드시 Secret으로 관리)
  - 개발: 테스트용 값, 운영: 실제 보안 키

---

## 6. 기타(필요 시)

- **AUTH_SERVER_URL**
  - 인증 서버 주소 (remote 모드에서 필요)
- **AUTH_LOCAL_TOKEN**
  - 로컬 인증 토큰 (local 모드에서 필요)
- **OTLP_ENDPOINT**
  - OTEL OTLP 익스포트 엔드포인트 (OTEL_EXPORTER가 otlp/tempo 등일 때)

---

## 사용 및 적용 방법

- 위 값들은 모두 `.env` 파일(개발) 또는 K8s ConfigMap/Secret(운영)에 반드시 명시해야 합니다.
- 값이 누락되거나 잘못 설정되면 서비스가 정상 동작하지 않거나, 실서비스 연동이 되지 않을 수 있습니다.
- 운영/스테이지 환경에서는 Sentry, OTEL, Kafka, MinIO, DB, JWT_SECRET 등 민감 정보는 반드시 Secret으로 관리하세요.

---

이 문서를 참고하여 포팅 시 환경변수 및 주요 값을 빠짐없이 점검·설정하세요.
