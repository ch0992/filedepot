#!/bin/bash
set -e

DOCKER_BUILDKIT=1 docker build -t filedepot-log:local -f app/services/log/Dockerfile .
echo "[빌드 완료] filedepot-log 이미지 생성 (태그: :local)"
