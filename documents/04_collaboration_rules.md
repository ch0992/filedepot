# 04. Collaboration Rules

filedepot 프로젝트 협업 및 PR 리뷰를 위한 규칙을 안내합니다.

## 브랜치 전략
- main: 운영 배포용, 직접 push 금지
- dev: 통합 개발, 기능 병합 전 테스트 필수
- feature/{name}: 기능별 작업, 완료 후 dev로 PR

## 커밋 메시지 규칙
- [타입] 간단 요약 (ex. [feat] 파일 업로드 기능 추가)
- 타입: feat, fix, docs, refactor, test, chore 등
- 상세 변경 내역은 본문에 추가

## PR 리뷰 정책
- 최소 1인 이상 리뷰 승인 후 병합
- 리뷰어는 체크리스트(02_review_checklist.md) 기반 검토
- 코드 컨벤션/문서 위반 시 수정 요청

## squash/rebase 기준
- dev → main 병합 시 squash 사용, 커밋 단순화
- feature → dev 병합 시 rebase 권장

---

> 본 문서는 filedepot 협업 및 코드리뷰 정책을 안내합니다. (자동 생성)
