#!/bin/bash
set -e

echo "[deploy_k8s_log] Log 서비스 K8S 배포 시작"
kubectl apply -f k8s/log-deployment.yaml
kubectl rollout restart deployment/log -n filedepot
kubectl rollout status deployment/log -n filedepot
echo "[deploy_k8s_log] Log 서비스 K8S 배포 완료"
