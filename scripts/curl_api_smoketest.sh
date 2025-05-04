#!/bin/bash
set -e

API_BASE="http://localhost:8000"
TOKEN="test-access-token"

function api_get() {
  echo -e "\n### GET $1"
  curl -s -w '\nHTTP %{http_code}\n' -H "Authorization: Bearer $TOKEN" "$API_BASE$1"
}

function api_post() {
  echo -e "\n### POST $1"
  curl -s -w '\nHTTP %{http_code}\n' -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "$2" "$API_BASE$1"
}

# file 서비스
api_get "/file/imgplt/aliases"
api_get "/file/imgplt/s3/test.txt"
api_get "/file/imgplt/zips?sql=SELECT%20*%20FROM%20files"
api_get "/file/imgplt/sqls?query=SELECT%20*%20FROM%20files"
api_post "/file/topics/test-topic" '{"file_id": "example_id", "size": 123}'
api_get "/file/ping"

# data 서비스
api_get "/data/topics"
api_post "/data/topics/test-table" '{"order_id": "order123", "user_id": "user456", "amount": 100}'
api_post "/data/sqls" '{"sql": "SELECT * FROM data"}'
api_post "/data/curs" '{"query": "SELECT * FROM data", "cursor": null}'
api_get "/data/ping"

# auth 서비스
api_get "/auth/imgplt/auths"

# log 서비스
api_post "/log/event" '{"event": "test-event"}'
api_get "/log/ping"

# 기타 내부/테스트 엔드포인트
api_get "/imgplt/test/sentry"
api_get "/imgplt/test-trace"
api_get "/imgplt/log-test"
api_get "/internal-test/hello"
api_get "/gateway/ping"
