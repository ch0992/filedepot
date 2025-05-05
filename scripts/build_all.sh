#!/bin/bash
set -e

# <none> 태그의 dangling 이미지 모두 삭제
if [[ $(docker images -f "dangling=true" -q | wc -l) -gt 0 ]]; then
  echo "[정리] <none> 태그의 Docker 이미지 삭제 중..."
  docker rmi $(docker images -f "dangling=true" -q) || true
else
  echo "[정리] 삭제할 <none> 이미지가 없습니다."
fi

# 빌드: gateway (병렬)
echo "[병렬 빌드 시작] gateway, file, data, log"
DOCKER_BUILDKIT=1 docker build -t filedepot-gateway:local -f app/services/gateway/Dockerfile . &
PID_GATEWAY=$!
DOCKER_BUILDKIT=1 docker build -t filedepot-file:local -f app/services/file/Dockerfile . &
PID_FILE=$!
DOCKER_BUILDKIT=1 docker build -t filedepot-data:local -f app/services/data/Dockerfile . &
PID_DATA=$!
DOCKER_BUILDKIT=1 docker build -t filedepot-log:local -f app/services/log/Dockerfile . &
PID_LOG=$!

wait $PID_GATEWAY $PID_FILE $PID_DATA $PID_LOG

echo "[병렬 빌드 완료] filedepot-gateway, file, data, log 이미지 생성 (태그: :local)"
