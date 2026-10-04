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

humanaapparels.com lives in its own Cloudflare account, so it has its own
tunnel, run by the `cloudflared` service in `docker-compose.yml` (profile
`tunnel`), separate from the server's system cloudflared used by other sites.

1. Cloudflare (humanaapparels account) → Zero Trust → Networks → Tunnels →
   Create tunnel (Cloudflared) → copy the token.
2. Public hostnames: `humanaapparels.com` and `www.humanaapparels.com` →
   service `HTTP` / `web:8000`. Leave mail records (MX, SPF/DMARC TXT,
   autodiscover and DKIM CNAMEs) untouched and DNS-only.
3. Switch `.env` to the `docker/env.production.example` values (keep the
   existing `SECRET_KEY` and `POSTGRES_PASSWORD`), set
   `COMPOSE_PROFILES=tunnel` and `CLOUDFLARE_TUNNEL_TOKEN`, then run
   `bash scripts/deploy-docker.sh`.

With `SECURE_SSL_REDIRECT=true`, http://192.168.245.25:3003 redirects to
HTTPS, so use the domain (admin included) from then on.
