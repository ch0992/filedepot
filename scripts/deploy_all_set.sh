#!/bin/bash
set -e

# 1. 전체 빌드
bash scripts/build_all.sh

# 2. 전체 K8s 배포
bash scripts/deploy_k8s_all.sh

# 3. gateway 포트포워딩 재시작
bash scripts/portforward_restart.sh

echo "[완료] 전체 빌드, 배포, 포트포워딩 재시작까지 완료!"
