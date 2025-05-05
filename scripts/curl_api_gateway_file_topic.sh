#!/bin/bash
set -e

API_BASE="http://localhost:8000"
TOKEN="dev-token"

function api_post() {
  echo -e "\n### POST $1"
  curl -s -w '\nHTTP %{http_code}\n' -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "$2" "$API_BASE$1"
}

# gateway -> file -> Kafka FastStream 연동 테스트
api_post "/gateway/topics/test" '{"file_id": "testfile1", "user_id": "testuser", "size": 12345, "metadata": {"key": "value"}}'
