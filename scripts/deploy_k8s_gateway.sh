#!/bin/bash
set -e

echo "[deploy_k8s_gateway] Gateway 서비스 K8S 배포 시작"
kubectl rollout restart deployment/gateway -n filedepot
kubectl rollout status deployment/gateway -n filedepot
echo "[deploy_k8s_gateway] Gateway 서비스 K8S 배포 완료"
