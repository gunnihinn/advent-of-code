#!/usr/bin/env bash

set -euo pipefail

day=$(seq -f "%05g" $1 $1)

mkdir -p "$day"
cp main.cpp "$day"
