#!/bin/bash

set -e

echo "[1] kubectl 클러스터 상태 점검"
kubectl cluster-info || {
    echo "❌ 클러스터가 실행 중이 아닙니다. Docker Desktop/Kind를 재시작하세요."
    exit 1
}

echo "[2] 기존 8000 포트 포워딩 프로세스만 안전하게 종료"
PIDS=$(ps aux | grep 'kubectl port-forward.*8000:8000' | grep -v grep | awk '{print $2}')
if [ -n "$PIDS" ]; then
    echo "🔪 kubectl port-forward 프로세스 종료: $PIDS"
    kill $PIDS
else
    echo "✅ 기존 포트포워딩 프로세스 없음"
fi

echo "[3] 포트포워딩 재시작 (백그라운드)"
nohup kubectl port-forward svc/gateway 8000:8000 -n filedepot > port-forward.log 2>&1 &

sleep 2
echo "[4] 포트포워딩 상태 확인"
lsof -i :8000 || echo "포트포워딩 프로세스가 아직 없음 (잠시 후 재확인)"

echo "[완료] http://localhost:8000 에서 gateway API 접근 가능"
