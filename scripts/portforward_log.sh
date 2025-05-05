#!/bin/bash
set -e

echo "[portforward_log] Log 서비스 포트포워딩 시작"
kubectl port-forward svc/log 8003:8003 -n filedepot &
echo "[portforward_log] Log 서비스 포트포워딩 완료 (http://localhost:8003)"
