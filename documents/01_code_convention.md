# 01. Code Convention

filedepot 프로젝트의 코드 작성 규칙을 아래와 같이 안내합니다. 초보자도 쉽게 적용할 수 있도록 예시와 함께 설명합니다.

## 1. Import 정렬 순서
- 표준 라이브러리 → 서드파티 → 로컬 모듈 순
```python
import os
import typing

import fastapi
import pydantic

from app.file.services.interfaces import FileService
```

## 2. 주석 가이드
- 함수/클래스, 주요 로직에 한글 주석 권장
- "왜"와 "어떻게"를 간결히 설명
```python
# 파일 업로드 처리 함수
async def upload_file(...):
    ...
```

## 3. 함수/변수 명명 규칙
- 소문자+언더스코어(snake_case) 사용
- 비동기 함수는 async/await 활용

## 4. 타입 힌트
- 모든 함수 인자/반환값에 타입 힌트 명시
```python
def get_file_meta(file_id: str) -> dict:
    ...
```

## 5. 예외 처리 패턴
- FastAPI HTTPException, Pydantic ValidationError 적극 활용
- 예외 발생 시 로깅 및 Sentry 연동 권장
```python
from fastapi import HTTPException

if not valid:
    raise HTTPException(status_code=400, detail="Invalid input")
```

## 6. 스타일 가이드(서비스별)
- FastAPI: APIRouter, 의존성 주입 활용
- Pydantic: BaseModel 상속, 필드 타입 명확히
- Kafka: 메시지 스키마 명확화, topic 상수화
- OpenTelemetry: trace-id 전달, context 관리

---

> 본 문서는 filedepot 코드 컨벤션을 예시와 함께 안내합니다. (자동 생성)
