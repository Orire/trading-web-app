# TradingAPP_Ri VM Deployment (Isolated Tenant)

This deployment is intentionally isolated from all other projects on the host.

## Isolation Contract

- Linux user/group: `tradingapp_ri`
- App root: `/opt/tradingapp-ri`
- Env directory: `/etc/tradingapp-ri`
- Logs: `/var/log/tradingapp-ri`
- Services:
  - `tradingapp-ri-backend.service`
  - `tradingapp-ri-frontend.service`
- Nginx site file: `/etc/nginx/sites-available/tradingapp-ri.conf`

Do not reuse directories, users, service names, or env files from any other project.

## One-Time Provisioning

```bash
cd /opt/tradingapp-ri/repo
sudo bash ops/vm/install-tradingapp-ri.sh
```

## Env Setup

```bash
sudo mkdir -p /etc/tradingapp-ri
sudo cp ops/vm/backend.env.example /etc/tradingapp-ri/backend.env
sudo cp ops/vm/frontend.env.example /etc/tradingapp-ri/frontend.env
sudo chown root:tradingapp_ri /etc/tradingapp-ri/*.env
sudo chmod 640 /etc/tradingapp-ri/*.env
```

## Deploy/Update

```bash
cd /opt/tradingapp-ri/repo
bash ops/vm/deploy-tradingapp-ri.sh
```

## Verify

```bash
systemctl status tradingapp-ri-backend.service --no-pager
systemctl status tradingapp-ri-frontend.service --no-pager
curl -fsS http://127.0.0.1:8000/health
curl -I http://127.0.0.1:3000
```

## Optional Public HTTPS

1. Copy `ops/vm/nginx-tradingapp-ri.conf` to `/etc/nginx/sites-available/tradingapp-ri.conf`.
2. Update domain placeholders.
3. Enable site and reload nginx.
4. Issue certificate with certbot:

```bash
sudo certbot --nginx -d tradingapp-ri.example.com -d www.tradingapp-ri.example.com
```
