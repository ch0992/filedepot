#!/bin/bash
set -e

bash scripts/build_log.sh
bash scripts/deploy_k8s.sh log
