#!/bin/bash
set -e

# ============================
# YAHAN APNI INFO BHARO
# ============================
GH_USER="muzammilxd001-bit"
GH_TOKEN="YAHAN_TOKEN_PASTE_KARO"
GH_EMAIL="YAHAN_EMAIL_LIKHO"
# ============================

REPO_URL="https://${GH_USER}:${GH_TOKEN}@github.com/muzammilxd001-bit/hangouts.git"

echo "=== Git setup ==="
git config --global user.name "$GH_USER"
git config --global user.email "$GH_EMAIL"

if [ ! -d ".git" ]; then
    git init
fi

git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

git add .
git commit -m "Ignis Bot initial commit" 2>/dev/null || echo "Already committed."

echo "=== Pushing to GitHub ==="
git push -u origin main --force

echo ""
echo "Done! Check: https://github.com/muzammilxd001-bit/hangouts"
