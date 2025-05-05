#!/bin/bash
set -e

echo "[build_file] File 서비스 Docker 이미지 빌드 시작"
docker build -t filedepot-file:local -f Dockerfile.file .
echo "[build_file] File 서비스 Docker 이미지 빌드 완료"
