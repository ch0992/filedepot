#!/bin/bash
# Run ruff lint check for the filedepot project
# Usage: bash scripts/lint_check.sh

set -e

# Lint all Python files in the project root and app directory
ruff check .
