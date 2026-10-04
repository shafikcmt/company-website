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

Add a public hostname `humanaapparels.com` (and `www`) → `http://localhost:3003`
on the tunnel, then switch `.env` to `docker/env.production.example` values
(DJANGO_ENV=production, HTTPS cookies, `SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https`)
and run the deploy script again.
