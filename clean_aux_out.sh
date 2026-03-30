#!/bin/bash
set -euo pipefail

BASE_DIR="${1:-.}"

#for dir in "$BASE_DIR/auxil" "$BASE_DIR/out"; do
#  if [ -d "$dir" ]; then
#    echo "Cleaning: $dir"
#    find "$dir" -mindepth 1 -delete
#  else
#    echo "Skipping missing directory: $dir"
#  fi
#done
#
#echo "Done."