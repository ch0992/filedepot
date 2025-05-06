# 03. Example Walkthrough

아래는 `/imgplt/meta/{topic}` API를 예시로 gateway → 인증 → 비즈니스 로직 → kafka 발행 → 로그/예외 흐름을 상세히 해설합니다.

## 1. Gateway 라우트 예시
```python
@router.post("/imgplt/meta/{topic}")
async def upload_meta(topic: str, meta: MetaModel, user=Depends(auth)):
    tracer.start_span("upload_meta")
    result = await file_service.upload_meta(topic, meta, user)
    return {"result": result}
```

## 2. 인증 처리
- `Depends(auth)`로 JWT 등 인증 수행, 실패 시 401 반환

## 3. 비즈니스 로직 호출
- file_service에서 메타 저장 및 kafka 발행

## 4. Kafka 메시지 발행 예시
```python
await kafka_producer.send(topic, meta.dict())
```

## 5. 트레이싱/로깅/예외 처리
- tracer로 trace-id 전달, 예외 발생 시 Sentry로 에러 전송
```python
try:
    ...
except Exception as e:
    tracer.record_exception(e)
    sentry_sdk.capture_exception(e)
    raise HTTPException(status_code=500, detail="Internal Error")
```

---

> 본 문서는 filedepot의 실제 API 흐름 예시를 상세 해설합니다. (자동 생성)
