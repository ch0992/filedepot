#!/bin/bash
set -e

echo "[portforward_data] Data 서비스 포트포워딩 시작"
kubectl port-forward svc/data 8002:8002 -n filedepot &
echo "[portforward_data] Data 서비스 포트포워딩 완료 (http://localhost:8002)"
