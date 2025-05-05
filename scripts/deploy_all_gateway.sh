#!/bin/bash
set -e

bash scripts/build_gateway.sh
bash scripts/deploy_k8s_gateway.sh
bash scripts/portforward_gateway.sh
