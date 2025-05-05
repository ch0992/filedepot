#!/bin/bash
set -e

echo "[build_gateway] Gateway 서비스 Docker 이미지 빌드 시작"
docker build -t filedepot-gateway:local -f Dockerfile.gateway .
echo "[build_gateway] Gateway 서비스 Docker 이미지 빌드 완료"
