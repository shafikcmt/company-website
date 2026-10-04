"""Validated environment settings; no database connections or filesystem writes."""

import ipaddress
import os
import re
from urllib.parse import urlsplit

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key


def boolean(env, name, default):
    value = env.get(name, str(default)).strip().lower()
    if value not in {"true", "false", "1", "0"}:
        raise ImproperlyConfigured(f"{name} must be true, false, 1 or 0")
    return value in {"true", "1"}


def integer(env, name, default):
    value = env.get(name, str(default)).strip()
    if not re.fullmatch(r"[0-9]+", value):
        raise ImproperlyConfigured(f"{name} must be a non-negative integer")
    return int(value)


def comma_list(env, name, default=""):
    value = env.get(name, default).strip()
    if not value:
        return []
    items = [item.strip() for item in value.split(",")]
    if any(not item for item in items):
        raise ImproperlyConfigured(f"{name} contains an empty list entry")
    return items


def valid_host(host):
    if host == "*":
        return True
    if host.startswith("[") and host.endswith("]"):
        try:
            return ipaddress.ip_address(host[1:-1]).version == 6
        except ValueError:
            return False
    host = host.removeprefix(".").removesuffix(".")
    return bool(host) and len(host) <= 253 and all(
        re.fullmatch(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", label)
        for label in host.split(".")
    )


def origins(env, name, production):
    values = comma_list(env, name)
    for value in values:
        try:
            parsed = urlsplit(value)
            port = parsed.port  # Validate malformed/out-of-range ports.
            valid = (
                parsed.scheme in ({"https"} if production else {"http", "https"})
                and parsed.hostname
                and valid_host(parsed.hostname if ":" not in parsed.hostname else f"[{parsed.hostname}]")
                and not parsed.username and not parsed.password
                and not parsed.path and not parsed.query and not parsed.fragment
                and "*" not in parsed.netloc
                and (port is None or port > 0)
            )
        except ValueError:
            valid = False
        if not valid:
            raise ImproperlyConfigured(f"{name} must contain explicit HTTP(S) origins; production requires HTTPS")
    return values


def read_environment(base_dir, environ=None):
    env = os.environ if environ is None else environ
    mode = env.get("DJANGO_ENV", "development").strip().lower()
    if mode not in {"development", "production"}:
        raise ImproperlyConfigured("DJANGO_ENV must be development or production")
    production = mode == "production"
    debug = boolean(env, "DEBUG", not production)
    if production and debug:
        raise ImproperlyConfigured("DEBUG must be false in production")

    secret = env.get("SECRET_KEY", "")
    if production and (
        len(secret) < 50 or len(set(secret)) < 5
        or secret.startswith("django-insecure-") or secret != secret.strip()
    ):
        raise ImproperlyConfigured("Production requires a persistent, strong SECRET_KEY")

    hosts = comma_list(env, "ALLOWED_HOSTS", "" if production else "localhost,127.0.0.1,[::1]")
    if any(not valid_host(host) for host in hosts) or (production and (not hosts or "*" in hosts)):
        raise ImproperlyConfigured("ALLOWED_HOSTS must contain valid explicit hosts in production")

    url = env.get("DATABASE_URL")
    if url is None and not production:
        url = f"sqlite:///{base_dir / 'db.sqlite3'}"
    if not url or not url.strip():
        raise ImproperlyConfigured("DATABASE_URL is required; SQLite fallback is development-only")
    try:
        database = dj_database_url.parse(url, conn_max_age=600)
    except (ValueError, KeyError, TypeError):
        # Never expose a URL that may contain database credentials.
        raise ImproperlyConfigured("DATABASE_URL is invalid") from None
    if not database.get("NAME"):
        raise ImproperlyConfigured("DATABASE_URL must identify a database")
    if production and database.get("ENGINE") != "django.db.backends.postgresql":
        raise ImproperlyConfigured("Production DATABASE_URL must configure PostgreSQL")

    session_secure = boolean(env, "SESSION_COOKIE_SECURE", production)
    csrf_secure = boolean(env, "CSRF_COOKIE_SECURE", production)
    if production and not (session_secure and csrf_secure):
        raise ImproperlyConfigured("Production session and CSRF cookies must be secure")

    proxy = comma_list(env, "SECURE_PROXY_SSL_HEADER")
    if proxy and proxy != ["HTTP_X_FORWARDED_PROTO", "https"]:
        raise ImproperlyConfigured("SECURE_PROXY_SSL_HEADER must be empty or HTTP_X_FORWARDED_PROTO,https")
    hsts_seconds = integer(env, "SECURE_HSTS_SECONDS", 0)
    hsts_subdomains = boolean(env, "SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
    hsts_preload = boolean(env, "SECURE_HSTS_PRELOAD", False)
    if (hsts_subdomains or hsts_preload) and not hsts_seconds:
        raise ImproperlyConfigured("HSTS subdomains/preload require positive SECURE_HSTS_SECONDS")

    return {
        "DJANGO_ENV": mode,
        "SECRET_KEY": secret or get_random_secret_key(),
        "DEBUG": debug,
        "ALLOWED_HOSTS": hosts,
        "CSRF_TRUSTED_ORIGINS": origins(env, "CSRF_TRUSTED_ORIGINS", production),
        "CORS_ALLOWED_ORIGINS": origins(env, "CORS_ALLOWED_ORIGINS", production),
        "DATABASE_URL": url,
        "DATABASES": {"default": database},
        "SESSION_COOKIE_SECURE": session_secure,
        "CSRF_COOKIE_SECURE": csrf_secure,
        "SECURE_SSL_REDIRECT": boolean(env, "SECURE_SSL_REDIRECT", production),
        "SECURE_PROXY_SSL_HEADER": tuple(proxy) if proxy else None,
        "SECURE_HSTS_SECONDS": hsts_seconds,
        "SECURE_HSTS_INCLUDE_SUBDOMAINS": hsts_subdomains,
        "SECURE_HSTS_PRELOAD": hsts_preload,
    }
