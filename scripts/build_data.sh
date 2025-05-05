#!/bin/bash
set -e

echo "[build_data] Data 서비스 Docker 이미지 빌드 시작"
docker build -t filedepot-data:local -f Dockerfile.data .
echo "[build_data] Data 서비스 Docker 이미지 빌드 완료"
