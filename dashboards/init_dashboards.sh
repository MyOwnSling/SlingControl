#!/bin/bash
set -e
DIR="$( cd "$(dirname $0)" && pwd )"

# Tipboard config
[ -z "$1" ] && exit 3
SETTINGS_SRC="${DIR}/settings-local_src.py"
SETTINGS="${DIR}/settings-local.py"
cp "${SETTINGS_SRC}" "${SETTINGS}"
echo "API_KEY = '$1'" >> "${SETTINGS}"
