#!/bin/bash
set -e

echo "[deploy_k8s_data] Data 서비스 K8S 배포 시작"
kubectl apply -f k8s/data-deployment.yaml
kubectl rollout restart deployment/data -n filedepot
kubectl rollout status deployment/data -n filedepot
echo "[deploy_k8s_data] Data 서비스 K8S 배포 완료"
