#!/usr/bin/env bash

set -eu -o pipefail

function generate() {
  local new_api_dir
  new_api_dir="$(dirname "$0")"
  pushd "${new_api_dir}"

  uv sync
  # shellcheck disable=SC1091
  source .venv/bin/activate

  # python3 merge_apis.py ecd

  local -a prods=()
  prods+=(ecd)
  prods+=(ecd-20201002)
  prods+=(eds-user)
  prods+=(workorder)

  local prod
  for prod in "${prods[@]}"; do
    python3 convert_api.py "${prod}"
  done

  deactivate
}

generate
