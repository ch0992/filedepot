#!/bin/bash
set -e

bash scripts/build_file.sh
bash scripts/deploy_k8s_file.sh
bash scripts/portforward_file.sh
