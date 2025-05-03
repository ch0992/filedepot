#!/bin/bash
set -e

NAMESPACE="filedepot"
CONFIGMAP_NAME="filedepot-env"

# 1. .env 파일을 ConfigMap으로 생성/업데이트
kubectl create configmap $CONFIGMAP_NAME --from-env-file=.env -n $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

echo "[INFO] ConfigMap $CONFIGMAP_NAME updated in namespace $NAMESPACE."

# 2. 전체 서비스 rollout restart 및 상태 확인
echo "[INFO] Restarting deployments: gateway, file, data, log"
for svc in gateway file data log; do
  kubectl -n $NAMESPACE rollout restart deployment $svc
  echo "[INFO] $svc deployment restarted."
  echo "[INFO] Waiting for $svc pod to be ready (readinessProbe)..."
  kubectl -n $NAMESPACE rollout status deployment $svc
  echo "[INFO] $svc pod is ready."
done

# 3. gateway 접근성 체크 및 무조건 포트포워딩 재설정 (외부 접근 필요 서비스만)
CHECK_URL="http://localhost:8000/gateway/ping"
HTTP_OK=$(curl -s -o /dev/null -w "%{http_code}" --max-time 2 "$CHECK_URL" || true)
if [ "$HTTP_OK" = "200" ]; then
  echo "[INFO] Gateway API is already accessible at $CHECK_URL (HTTP 200)"
else
  echo "[WARN] Gateway API not accessible at $CHECK_URL. Forcing port-forward reset..."
  # 8000번 포트를 점유 중인 모든 프로세스 종료
  PIDS_8000=$(lsof -ti tcp:8000 || true)
  if [ -n "$PIDS_8000" ]; then
    echo "[INFO] Killing processes using port 8000: $PIDS_8000"
    kill -9 $PIDS_8000 || true
  fi
  # 기존 kubectl port-forward 프로세스 종료
  PORT_FORWARD_PIDS=$(pgrep -f "kubectl -n $NAMESPACE port-forward svc/gateway 8000:8000" || true)
  if [ -n "$PORT_FORWARD_PIDS" ]; then
    echo "[INFO] Killing existing kubectl port-forward processes: $PORT_FORWARD_PIDS"
    kill -9 $PORT_FORWARD_PIDS || true
  fi
  # 새로 포트포워딩 실행
  echo "[INFO] Starting new port-forward for gateway:8000..."
  nohup kubectl -n $NAMESPACE port-forward svc/gateway 8000:8000 > /dev/null 2>&1 &
  sleep 2
  NEW_PID=$(pgrep -f "kubectl -n $NAMESPACE port-forward svc/gateway 8000:8000")
  if [ -n "$NEW_PID" ]; then
    echo "[INFO] Port-forward started (PID: $NEW_PID). Access gateway at http://localhost:8000"
  else
    echo "[ERROR] Failed to start port-forward for gateway:8000" >&2
  fi
fi
