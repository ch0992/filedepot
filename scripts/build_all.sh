#!/bin/bash
set -e

# 0. 기존 filedepot 관련 컨테이너 안전 종료 및 이미지 삭제
echo "[정리] 기존 filedepot 관련 컨테이너/이미지 정리..."
for svc in gateway file data log; do
  container_id=$(docker ps -q -f "name=filedepot-$svc")
  if [ -n "$container_id" ]; then
    echo "Stopping running container $container_id for $svc"
    docker stop $container_id
    docker rm $container_id
  fi
  image_id=$(docker images -q filedepot-$svc:local)
  if [ -n "$image_id" ]; then
    echo "Removing image $image_id for $svc"
    docker rmi $image_id || true
  fi
  sleep 1
  # 혹시 남아있는 dangling image도 정리
  dangling=$(docker images -f "dangling=true" -q)
  if [ -n "$dangling" ]; then
    echo "[정리] <none> 태그의 Docker 이미지 삭제 중..."
    docker rmi $dangling || true
  fi
  sleep 1
  done

# 빌드: gateway, file, data, log (병렬)
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
