# filedepot 프로젝트 OpenTelemetry 기반 로깅/트레이싱/예외 추적 검증 체크리스트

## 1. 테스트 실행
- `pytest tests/log/test_logging_injection.py` 명령어로 통합 테스트를 실행합니다.
- 또는 curl/Postman 등으로 직접 주요 엔드포인트를 호출해도 무방합니다.

---

## 2. 로그/트레이스 확인 항목

### [A] stdout 또는 로그 파일 확인
- 각 API 호출 시 아래와 같은 로그가 출력되는지 확인합니다:
  - `trace_id=...`, `span_id=...` 필드가 로그 메시지에 포함되어야 함
  - 예시:
    ```
    INFO trace_id=123456789 span_id=987654321 "message": ...
    ```
- 로그 레벨, 서비스명, 엔드포인트명 등도 함께 출력되는지 확인

### [B] 예외/오류 발생 시
- 의도적으로 에러를 발생시키는 엔드포인트(예: /test/sentry, 잘못된 파라미터 등) 호출
- 로그에 capture_and_log 호출 흔적, 에러 메시지, Sentry 전송 로그가 남는지 확인

### [C] Sentry(또는 연동된 APM/모니터링) 콘솔 확인
- 예외 발생 시 Sentry 대시보드(또는 연동된 외부 모니터링)에서 이벤트가 정상적으로 수집되는지 확인

### [D] 환경 변수/설정에 따른 trace/log exporter 동작 확인
- .env 또는 환경 변수로 OTEL_EXPORTER, LOG_LEVEL 등을 변경 후
- Jaeger, stdout, OpenSearch 등 각 exporter로 trace/log가 정상 전송되는지 확인

---

## 3. 인증/트레이서 실행 순서 확인
- Authorization 헤더가 정상적으로 처리된 후 tracer가 실행되는지 로그에서 순서 확인

---

## 4. (선택) 로그 포맷/구조화 검증
- 로그가 JSON 등 구조화 포맷으로 출력되는지, trace_id/서비스명/엔드포인트명 등 필드가 일관되게 포함되는지 확인

---

### 💡 참고
- 모든 엔드포인트(health check 포함)에서 위 항목이 일관되게 동작해야 합니다.
- 장애 상황, 정상 상황 모두에서 trace/log/sentry 전송이 잘 남는지 반드시 직접 확인하세요.
