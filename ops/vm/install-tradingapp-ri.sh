#!/usr/bin/env bash
set -euo pipefail

APP_USER="tradingapp_ri"
APP_GROUP="tradingapp_ri"
APP_ROOT="/opt/tradingapp-ri"
REPO_DIR="$APP_ROOT/repo"
ENV_DIR="/etc/tradingapp-ri"
LOG_DIR="/var/log/tradingapp-ri"

echo "[1/7] Installing system packages..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip nodejs npm nginx

echo "[2/7] Creating isolated user and directories..."
if ! id "$APP_USER" >/dev/null 2>&1; then
  sudo useradd --system --create-home --home-dir "$APP_ROOT" --shell /usr/sbin/nologin "$APP_USER"
fi

sudo mkdir -p "$APP_ROOT" "$ENV_DIR" "$LOG_DIR"
sudo chown -R "$APP_USER:$APP_GROUP" "$APP_ROOT" "$LOG_DIR"
sudo chmod 750 "$ENV_DIR"

echo "[3/7] Verifying repository path..."
if [ ! -d "$REPO_DIR" ]; then
  echo "Missing repository at $REPO_DIR"
  echo "Clone your tenant repo there first:"
  echo "  sudo -u $APP_USER git clone git@github.com:Orire/trading-web-app.git $REPO_DIR"
  exit 1
fi

echo "[4/7] Installing backend dependencies..."
sudo -u "$APP_USER" bash -lc "cd '$REPO_DIR/backend' && python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

echo "[5/7] Installing frontend dependencies/build..."
sudo -u "$APP_USER" bash -lc "cd '$REPO_DIR/frontend' && npm ci && npm run build"

echo "[6/7] Installing systemd services..."
sudo cp "$REPO_DIR/ops/vm/tradingapp-ri-backend.service" /etc/systemd/system/
sudo cp "$REPO_DIR/ops/vm/tradingapp-ri-frontend.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tradingapp-ri-backend.service tradingapp-ri-frontend.service

echo "[7/7] Done."
echo "Next:"
echo "  1) Create $ENV_DIR/backend.env and $ENV_DIR/frontend.env"
echo "  2) sudo systemctl restart tradingapp-ri-backend.service tradingapp-ri-frontend.service"
echo "  3) Configure nginx using ops/vm/nginx-tradingapp-ri.conf"
