#!/bin/bash
set -e

echo "[deploy_k8s_file] File 서비스 K8S 배포 시작"
kubectl apply -f k8s/file-deployment.yaml
kubectl rollout restart deployment/file -n filedepot
kubectl rollout status deployment/file -n filedepot
echo "[deploy_k8s_file] File 서비스 K8S 배포 완료"
