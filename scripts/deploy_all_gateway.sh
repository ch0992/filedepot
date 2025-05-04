#!/bin/bash
set -e

NAMESPACE="filedepot"
PORT=8000

# 1. gateway 빌드
bash scripts/build_gateway.sh

# 2. kind 클러스터에 최신 gateway 이미지 load
echo "[INFO] kind(filedepot)에 filedepot-gateway:local 이미지 load 시작..."
kind load docker-image filedepot-gateway:local --name filedepot

echo "[INFO] kind(filedepot)에 filedepot-gateway:local 이미지 load 완료."

# 3. gateway 배포 롤링 업데이트 및 상태 확인
kubectl -n $NAMESPACE rollout restart deployment gateway
kubectl -n $NAMESPACE rollout status deployment gateway

echo "[INFO] gateway 배포 및 상태 체크 완료"

# 4. gateway 포트포워딩 재시작 (공식 스크립트 사용)
bash scripts/portforward_restart.sh

echo "[완료] gateway 빌드, kind 이미지 반영, 배포, 포트포워딩까지 완료!"
