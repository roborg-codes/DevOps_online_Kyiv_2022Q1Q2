#!/bin/env bash

set -e

[[ ($# -eq 0) || ($# -gt 2) ]] && {
    USAGE=$(cat <<EOF
Usage:
    Enter sync directory and destination directory as arguments.
    Mind the trailing slashes. (see rsync manpages)
EOF)
    printf "%s\n" "$USAGE"
    exit 1
}

LOG_FILE="./sync.log"
SYNC_DIR="${1%/}"
TO_DIR="${2%/}"

rsync \
    -Cavz \
    --itemize-changes \
    --delete \
    "$SYNC_DIR" \
    "$TO_DIR" \
    | sed \
        -e 's/^>/transferring /' \
        -e 's/^</recieving /' \
        -e 's/^c/creating /' \
        -e 's/^\..*//' \
        -e 's/\*//' \
    | sed -r \
        -e 's/[f]{1}[\+\?\.]{9}/file/' \
        -e 's/[d]{1}[\+\?\.]{9}/directory/' \
    | tail -n +2 \
    | head -n -3 \
    | awk -v DATE="$(date)" '{print DATE " - " $0}' \
    | tee -ai "$LOG_FILE"
