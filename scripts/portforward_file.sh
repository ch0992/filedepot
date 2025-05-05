#!/bin/bash
set -e

echo "[portforward_file] File 서비스 포트포워딩 시작"
kubectl port-forward svc/file 8001:8001 -n filedepot &
echo "[portforward_file] File 서비스 포트포워딩 완료 (http://localhost:8001)"
