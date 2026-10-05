# Deployment (office server, Docker)

The site runs on the office server (`192.168.245.25`) with Docker Compose:
`db` (PostgreSQL 16) + `web` (Django/gunicorn on port 3003, also serving
`/static` and `/media`). Pushing to `master` deploys automatically through a
GitHub Actions self-hosted runner (`.github/workflows/deploy.yml`), which runs
`scripts/deploy-docker.sh`: pull, rebuild, migrate, collectstatic, health check.

## One-time server setup

```bash
cd ~/company-website
cp docker/env.internal.example .env      # then edit SECRET_KEY / POSTGRES_PASSWORD
DEPLOY_BRANCH=master bash scripts/deploy-docker.sh
docker compose exec web python manage.py createsuperuser
```

Self-hosted runner: GitHub repo → Settings → Actions → Runners → New
self-hosted runner (Linux), run the shown commands as user `hapl` with
`./config.sh ... --labels hapl-deploy`, then `sudo ./svc.sh install && sudo ./svc.sh start`.
The `hapl` user must be in the `docker` group and able to `git fetch`.

## Useful commands

```bash
docker compose ps
docker compose logs -f web
docker compose exec web python manage.py seed_content --clean   # demo data (wipes content)
docker compose exec db pg_dump -U hapl hapl > backup.sql         # database backup
```

## Public domain (Cloudflare Tunnel)

humanaapparels.com is served through the server's existing `cloudflared`
service (tunnel `moslamart`, also used by moslamart.com and ksa.shafiqul.dev).
The service reads `/etc/cloudflared/config.yml` (not `~/.cloudflared/`); the
site's rules sit before the final 404 rule:

```yaml
  - hostname: humanaapparels.com
    service: http://localhost:3003
  - hostname: www.humanaapparels.com
    service: http://localhost:3003
```

After editing: `sudo cloudflared --config /etc/cloudflared/config.yml tunnel ingress validate`
then `sudo systemctl restart cloudflared`.

Cloudflare DNS (zone humanaapparels.com, same account as the tunnel):

- `@` and `www`: CNAME → `3637430d-d86d-41e0-929e-2acbff274c3f.cfargotunnel.com`, proxied.
- Mail (Microsoft 365), all DNS only, never proxied: MX → `humanaapparels-com.mail.protection.outlook.com`,
  TXT SPF and `_dmarc`, CNAME `autodiscover`, `selector1._domainkey`,
  `selector2._domainkey`, and A `smtp` → 91.204.209.30.
- SSL/TLS mode: Full.

`.env` uses the `docker/env.production.example` values (HTTPS cookies,
`SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https`), so
http://192.168.245.25:3003 redirects to HTTPS; use the domain, admin included.

### Office network

The office DNS server (192.168.245.218, Active Directory) has its own
`humanaapparels.com` zone, so the bare domain resolves to the domain
controller inside the office. That zone has `www` A records →
104.21.74.146 and 172.67.159.96 (Cloudflare); inside the office use
https://www.humanaapparels.com.
