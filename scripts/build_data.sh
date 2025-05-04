#!/bin/bash
set -e

DOCKER_BUILDKIT=1 docker build -t filedepot-data:local -f app/services/data/Dockerfile .
echo "[빌드 완료] filedepot-data 이미지 생성 (태그: :local)"
