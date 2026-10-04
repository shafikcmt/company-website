#!/usr/bin/env bash
# Pull the latest code and rebuild/restart the containers.
# Run by the GitHub Actions self-hosted runner (.github/workflows/deploy.yml)
# or manually:  bash scripts/deploy-docker.sh
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
BRANCH="${DEPLOY_BRANCH:-master}"
cd "$APP_DIR"

if [ ! -f .env ]; then
  echo "Missing $APP_DIR/.env (copy docker/env.internal.example)." >&2
  exit 1
fi

echo "==> Updating code ($BRANCH)"
git fetch --prune origin "$BRANCH"
git checkout -B "$BRANCH" "origin/$BRANCH"
git reset --hard "origin/$BRANCH"   # tracked files only; .env, media/ and logs/ are untouched

mkdir -p media logs

echo "==> Building and starting containers"
docker compose up -d --build --remove-orphans

echo "==> Waiting for the site"
port="$(grep -E '^APP_PORT=' .env | cut -d= -f2 || true)"
port="${port:-3003}"
for i in $(seq 1 30); do
  if curl -fsS -o /dev/null "http://127.0.0.1:${port}/"; then
    echo "Site is up on port ${port}."
    docker image prune -f >/dev/null
    exit 0
  fi
  sleep 3
done

echo "Site did not respond; recent logs:" >&2
docker compose logs --tail=80 web >&2
exit 1
