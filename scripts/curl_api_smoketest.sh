#!/bin/bash
set -e

API_BASE="http://localhost:8000"
TOKEN="test-access-token"

function api_get() {
  echo -e "\n### GET $1"
  curl -s -w '\nHTTP %{http_code}\n' "$API_BASE$1"
}

function api_post() {
  echo -e "\n### POST $1"
  curl -s -w '\nHTTP %{http_code}\n' -X POST -H "Content-Type: application/json" -d "$2" "$API_BASE$1"
}

# file 서비스
# 최신 gateway 기반 API 테스트 스크립트
# 모든 엔드포인트는 gateway 경로 기준으로 테스트

# Gateway OpenAPI 기반 smoke test 스크립트

# 파일 관련
api_get "/gateway/file/imgplt/aliases"
api_get "/gateway/file/imgplt/s3/test.txt" # file_path = test.txt
api_get "/gateway/file/imgplt/zips?sql=SELECT%20*%20FROM%20files"
api_get "/gateway/file/imgplt/sqls?query=SELECT%20*%20FROM%20files"
api_get "/gateway/file/imgplt/aliases"

# 파일 메타데이터 Kafka 발행
api_post "/gateway/topics/test-topic" '{"file_id": "testfile1", "size": 12345, "user": "testuser"}'

# 데이터 관련
api_get "/gateway/data/topics"
api_post "/gateway/data/topics/test-table" '{"order_id": "order123", "user_id": "user456", "amount": 100}'

# Cursor 기반 대용량 데이터 조회
api_post "/gateway/imgplt/curs" '{"query": "SELECT * FROM big_table", "cursor": null}'

# 인증
api_get "/gateway/auth/imgplt/auths"

# 로그
api_post "/gateway/log/event" '{"event": "test-event"}'

# Health check
api_get "/gateway/ping"

