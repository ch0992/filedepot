# filedepot

FastAPI 기반 마이크로서비스 아키텍처(MSA) 프로젝트 스캐폴드입니다.

## 서비스 구조
- `file`: 파일 업로드/다운로드 (S3 MinIO)
- `data`: 메타 정보 및 SQL 처리 (PostgreSQL, Iceberg, OpenSearch)
- `log`: API 로그 수집 및 처리
- `gateway`: 인증/인가 처리 (JWT 기반)

## 공통 디렉토리
- `core/`, `db/`, `dependencies/`, `shared/`: 모든 서비스에서 공통 참조

## 인프라
- `infra/`, `charts/`, `manifests/`, `docker/`, `winds/`

---

각 주요 파일 및 디렉토리에는 placeholder와 역할 설명 주석이 포함되어 있습니다.
실제 구현은 각 서비스/공통 모듈에 추가해 주세요.
