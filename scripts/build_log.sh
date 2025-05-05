#!/bin/bash
set -e

echo "[build_log] Log 서비스 Docker 이미지 빌드 시작"
docker build -t filedepot-log:local -f Dockerfile.log .
echo "[build_log] Log 서비스 Docker 이미지 빌드 완료"
