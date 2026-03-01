#!/usr/bin/env bash
set -euo pipefail

APP_USER="tradingapp_ri"
REPO_DIR="/opt/tradingapp-ri/repo"

echo "[1/4] Pulling latest code from personal remote..."
git -C "$REPO_DIR" fetch personal
git -C "$REPO_DIR" checkout main
git -C "$REPO_DIR" reset --hard personal/main

echo "[2/4] Backend install/update..."
sudo -u "$APP_USER" bash -lc "cd '$REPO_DIR/backend' && source .venv/bin/activate && pip install -r requirements.txt"

echo "[3/4] Frontend install/build..."
sudo -u "$APP_USER" bash -lc "cd '$REPO_DIR/frontend' && npm ci && npm run build"

echo "[4/4] Restarting isolated services..."
sudo systemctl restart tradingapp-ri-backend.service
sudo systemctl restart tradingapp-ri-frontend.service

echo "Deployment complete."
echo "Verify:"
echo "  systemctl status tradingapp-ri-backend.service --no-pager"
echo "  systemctl status tradingapp-ri-frontend.service --no-pager"
echo "  curl -fsS http://127.0.0.1:8000/health"
