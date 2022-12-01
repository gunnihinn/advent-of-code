#!/usr/bin/env bash

set -euo pipefail

root="$(git rev-parse --show-toplevel)/2022"
day=$(seq -f "%02g" $1 $1)

mkdir -p "$root/$day"
cp "$root/main.cpp" "$root/$day"
