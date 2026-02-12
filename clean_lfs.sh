#!/usr/bin/env bash
set -euo pipefail

REPO_PATH="${1:-.}"

cd "$REPO_PATH"

git rev-parse --is-inside-work-tree >/dev/null
git lfs install >/dev/null 2>&1 || true

LFS_LIST_FILE="$(mktemp)"
git lfs ls-files -n > "$LFS_LIST_FILE"

if [ ! -s "$LFS_LIST_FILE" ]; then
  echo "No LFS-tracked files found"
  rm -f "$LFS_LIST_FILE"
  exit 0
fi

while IFS= read -r f; do
  if [ -n "$f" ]; then
    git rm -f -- "$f"
  fi
done < "$LFS_LIST_FILE"

rm -f "$LFS_LIST_FILE"

if [ -f .gitattributes ]; then
  ATTR_TMP="$(mktemp)"
  sed '/filter=lfs/d' .gitattributes > "$ATTR_TMP"
  mv "$ATTR_TMP" .gitattributes
  if [ ! -s .gitattributes ]; then
    rm -f .gitattributes
  fi
  git add -A
fi

git commit -m "Remove all Git LFS tracked files" || true

echo "Done. LFS-tracked files removed from the repo."