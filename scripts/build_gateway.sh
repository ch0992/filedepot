#!/bin/bash
set -e

DOCKER_BUILDKIT=1 docker build -t filedepot-gateway:local -f app/services/gateway/Dockerfile .
echo "[빌드 완료] filedepot-gateway 이미지 생성 (태그: :local)"
