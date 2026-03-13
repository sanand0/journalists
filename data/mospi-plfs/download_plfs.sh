#!/usr/bin/env bash
set -euo pipefail

URL="${PLFS_URL:-https://raw.githubusercontent.com/Vonter/india-plf-survey/main/data/plfs.parquet}"
OUTPUT_PATH="${1:-${OUTPUT_PATH:-plfs.parquet}}"
PARTIAL_PATH="${OUTPUT_PATH}.part"

file_size() {
  local path="$1"

  if [[ -f "$path" ]]; then
    wc -c < "$path" | tr -d '[:space:]'
  else
    echo 0
  fi
}

mkdir -p "$(dirname "$OUTPUT_PATH")"

REMOTE_SIZE="$(
  curl -fsSIL "$URL" |
    awk 'tolower($1) == "content-length:" { gsub("\r", "", $2); size = $2 } END { if (size != "") print size }'
)"

if [[ -z "$REMOTE_SIZE" ]]; then
  echo "Could not determine remote size for $URL" >&2
  exit 1
fi

if [[ -f "$OUTPUT_PATH" ]]; then
  LOCAL_SIZE="$(file_size "$OUTPUT_PATH")"
  if [[ "$LOCAL_SIZE" == "$REMOTE_SIZE" ]]; then
    echo "Already present: $OUTPUT_PATH ($LOCAL_SIZE bytes)"
    exit 0
  fi

  echo "Existing file does not match expected size: $OUTPUT_PATH ($LOCAL_SIZE of $REMOTE_SIZE bytes)" >&2
  echo "Remove or rename it, or pass a different output path." >&2
  exit 1
fi

PARTIAL_SIZE="$(file_size "$PARTIAL_PATH")"
if [[ "$PARTIAL_SIZE" -gt 0 ]]; then
  echo "Resuming download into $PARTIAL_PATH ($PARTIAL_SIZE of $REMOTE_SIZE bytes)"
else
  echo "Downloading $URL"
fi

curl -fL --retry 3 --retry-delay 2 -C - -o "$PARTIAL_PATH" "$URL"

FINAL_SIZE="$(file_size "$PARTIAL_PATH")"
if [[ "$FINAL_SIZE" != "$REMOTE_SIZE" ]]; then
  echo "Downloaded size mismatch: expected $REMOTE_SIZE bytes, got $FINAL_SIZE bytes" >&2
  exit 1
fi

mv "$PARTIAL_PATH" "$OUTPUT_PATH"
echo "Saved $OUTPUT_PATH ($FINAL_SIZE bytes)"
