#!/usr/bin/env bash

set -euo pipefail

root="$(git rev-parse --show-toplevel)/2022"
day=$(seq -f "%02g" $1 $1)

mkdir -p "$root/$day"
cp "$root/main.cpp" "$root/$day"
echo "add_executable($day $day/main.cpp)" >>"$root/CMakeLists.txt"

mv "~/Downloads/ex*" "$root/$day"
mv "~/Downloads/input" "$root/$day/input.txt"
