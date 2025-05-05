#!/bin/bash
set -e

echo "[portforward_gateway] Gateway 서비스 포트포워딩 시작"
kubectl port-forward svc/gateway 8000:8000 -n filedepot &
echo "[portforward_gateway] Gateway 서비스 포트포워딩 완료 (http://localhost:8000)"
