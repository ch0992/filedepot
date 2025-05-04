#!/bin/bash
set -e

DOCKER_BUILDKIT=1 docker build -t filedepot-file:local -f app/services/file/Dockerfile .
echo "[빌드 완료] filedepot-file 이미지 생성 (태그: :local)"
