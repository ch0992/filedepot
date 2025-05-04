#!/bin/bash
set -e

# 빌드: gateway
DOCKER_BUILDKIT=1 docker build -t filedepot-gateway:local -f app/services/gateway/Dockerfile .
# 빌드: file
DOCKER_BUILDKIT=1 docker build -t filedepot-file:local -f app/services/file/Dockerfile .
# 빌드: data
DOCKER_BUILDKIT=1 docker build -t filedepot-data:local -f app/services/data/Dockerfile .
# 빌드: log
DOCKER_BUILDKIT=1 docker build -t filedepot-log:local -f app/services/log/Dockerfile .

echo "[빌드 완료] filedepot-gateway, file, data, log 이미지 생성 (태그: :local)"
