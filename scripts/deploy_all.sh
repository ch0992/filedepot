#!/bin/bash
set -e

NAMESPACE=filedepot

# 1. 네임스페이스 생성
kubectl get ns $NAMESPACE >/dev/null 2>&1 || kubectl create namespace $NAMESPACE

# 2. ConfigMap 생성 (환경변수)
kubectl -n $NAMESPACE delete configmap filedepot-env --ignore-not-found
kubectl -n $NAMESPACE create configmap filedepot-env --from-env-file=.env

# 3. 서비스별 배포
echo "[쿠버네티스 배포] gateway"
kubectl -n $NAMESPACE apply -f k8s/gateway.yaml
echo "[쿠버네티스 배포] file"
kubectl -n $NAMESPACE apply -f k8s/file.yaml
echo "[쿠버네티스 배포] data"
kubectl -n $NAMESPACE apply -f k8s/data.yaml
echo "[쿠버네티스 배포] log"
kubectl -n $NAMESPACE apply -f k8s/log.yaml

# 4. 상태 확인
echo "[배포 상태]"
kubectl -n $NAMESPACE get pods

# 5. gateway 서비스 외부 노출 및 health check 테스트
echo "[gateway health check]"
NODE_PORT=$(kubectl -n $NAMESPACE get svc gateway -o jsonpath='{.spec.ports[0].nodePort}')
MINIKUBE_IP=$(minikube ip)
GATEWAY_URL="http://$MINIKUBE_IP:$NODE_PORT/gateway/ping"
echo "[curl] $GATEWAY_URL"
curl -i "$GATEWAY_URL"
