# Cloudflare Dynamic DNS Updater

This project automatically updates Cloudflare DNS records when your server's public IP changes. It uses Docker and the Cloudflare API to ensure your DNS records stay up-to-date.

---

## Features
- Automatically detects public IP changes using multiple services.
- Updates Cloudflare DNS records via API.
- Configurable update interval, TTL, and record type (A/AAAA).
- Dockerized for easy deployment.
- Supports `.env` file for secure configuration.

---

## Prerequisites
1. **Docker**: Install Docker from [https://www.docker.com](https://www.docker.com).
2. **Cloudflare API Token**: Create a token with **Edit zone DNS** permissions in your Cloudflare account.
3. **Zone ID and DNS Record ID**: Obtain these from your Cloudflare dashboard. You can obtain RecordID only with updating it in the dashboard, then it will be available in the Audit Log.

---

## Setup

1. **Clone the Repository**:

```bash
git clone https://github.com/yourusername/cloudflare-ddns.git
cd cloudflare-ddns
```

2. **Update variables in the `.env` file**:

```
# Required
CF_API_TOKEN=your_api_token
CF_ZONE_ID=your_zone_id
CF_DNS_RECORD_ID=your_record_id
CF_DNS_RECORD_NAME=subdomain.yourdomain.com

# Optional (with defaults)
CF_UPDATE_INTERVAL=300
CF_RECORD_TYPE=A
CF_TTL=1
CF_PROXIED=false
```

> [!WARNING]
> DO NOT STAGE THE .env FILE!
> It contains secrets.
> You can use `git update-index --assume-unchanged .env` to avoid staging it by accident.

3. **Build and Run**:
Use Docker Compose to build and start the service:

```bash
docker compose up -d
```

## Commands

**Start the Service**
```bash
docker compose up -d
```

**Stop the Service**
```bash
docker compose down
```

**View Logs**
```bash
docker compose logs -f
```

**Recreate the Service**
Use this after updating .env or making changes to the Dockerfile:

```bash
docker compose up -d --force-recreate
```

**Build the Docker Image**
```bash
docker compose build
```

