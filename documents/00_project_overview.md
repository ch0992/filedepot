# 00. Project Overview

filedepot는 대용량 파일 저장, 메타데이터 관리, 실시간 데이터 처리, 검색, 모니터링을 지원하는 모던 데이터 플랫폼입니다. 신규 팀원이 전체 구조와 흐름을 빠르게 이해할 수 있도록 주요 내용을 요약합니다.

## 아키텍처 및 서비스 구성

```
[Client]
   |
   v
[Gateway] <-> [File] <-> [S3]
     |            |
     v            v
[Data]        [Kafka] <-> [Flink]
     |            |
     v            v
[OpenSearch]  [Log]
     |
     v
  [Sentry]
```

- **Gateway**: 모든 API 진입점, 인증/인가, 트레이싱, 내부 서비스 호출
- **File**: 파일 업로드/다운로드, S3 연동, 메타데이터 관리, Kafka 메시지 발행
- **Data**: 메타/검색/통계, OpenSearch 연동, Kafka 메시지 발행
- **Log**: 서비스별 로그 수집, Sentry 연동
- **Kafka**: 이벤트 메시지 브로커, Flink와 연계
- **Flink**: 실시간 스트림 처리, Kafka 메시지 소비
- **S3**: 파일 영구 저장소
- **OpenSearch**: 데이터 인덱싱 및 검색
- **Sentry**: 에러 추적 및 모니터링

## API 흐름 예시
- 클라이언트 → Gateway → File/Data → S3/Kafka/OpenSearch → 응답/로깅/트레이싱

## 기술 스택
- Python, FastAPI, Pydantic, Kafka, S3, OpenSearch, Flink, Sentry, OpenTelemetry, Docker, Kubernetes

## 배포 전략
- 서비스별 Docker 컨테이너 개발/테스트
- Kubernetes(namespace: filedepot)에서 Pod 단위 배포
- Gateway를 통한 외부 접근 제한, Pod 간 내부 네트워크 연결

---

> 본 문서는 filedepot 프로젝트의 전체 구조와 흐름을 요약합니다. (자동 생성)
