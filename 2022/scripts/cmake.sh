#!/usr/bin/env bash

set -euo pipefail

root="$(git rev-parse --show-toplevel)/2022"

cmake -B "$root" -S "$root"
