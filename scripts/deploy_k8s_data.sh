#!/bin/bash
set -e

bash scripts/build_data.sh
bash scripts/deploy_k8s.sh data
