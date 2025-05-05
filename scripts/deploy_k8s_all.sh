#!/bin/bash
set -e

NAMESPACE="filedepot"
CONFIGMAP_NAME="filedepot-env"

# 1. .env 파일을 ConfigMap으로 생성/업데이트
kubectl create configmap $CONFIGMAP_NAME --from-env-file="$(dirname "$0")/../.env" -n $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

echo "[INFO] ConfigMap $CONFIGMAP_NAME updated in namespace $NAMESPACE."

# 2. kind 클러스터에 최신 이미지 load
# 병렬로 이미지 load
for svc in gateway file data log; do
  kind load docker-image filedepot-${svc}:local --name filedepot &
done
wait
echo "[INFO] 모든 이미지 병렬 load 완료."

# 3. 전체 서비스 rollout restart 및 상태 확인
echo "[INFO] Restarting deployments: gateway, file, data, log"
for svc in gateway file data log; do
  kubectl -n $NAMESPACE rollout restart deployment $svc
  echo "[INFO] $svc deployment restarted."
  echo "[INFO] Waiting for $svc pod to be ready (readinessProbe)..."
  kubectl -n $NAMESPACE rollout status deployment $svc
  echo "[INFO] $svc pod is ready."
done

# 기존 gateway 포트포워딩 프로세스 종료
PORT=8000
PF_PATTERN="kubectl port-forward.*$PORT:$PORT"
PIDS=$(pgrep -f "$PF_PATTERN")
if [ -n "$PIDS" ]; then
    echo "[INFO] Killing existing port-forward processes for gateway:$PORT ..."
    kill $PIDS
    sleep 1
fi

# 최신 gateway deployment로 포트포워딩 재설정
# (백그라운드 실행)
echo "[INFO] Starting new port-forward for gateway:$PORT..."
nohup kubectl -n $NAMESPACE port-forward deployment/gateway $PORT:$PORT > port-forward.log 2>&1 &
disown
echo "[INFO] Port-forward started. Access gateway at http://localhost:$PORT (log: port-forward.log)"
