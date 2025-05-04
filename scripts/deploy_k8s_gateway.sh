#!/bin/bash
set -e

bash scripts/build_gateway.sh

NAMESPACE="filedepot"
echo "[INFO] gateway 롤링 배포 시작"
kubectl -n $NAMESPACE rollout restart deployment gateway
kubectl -n $NAMESPACE rollout status deployment gateway

echo "[INFO] gateway 배포 완료"
