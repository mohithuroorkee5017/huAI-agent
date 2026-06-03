# HU Voice AI API - Deployment Guide

Complete guide for deploying HU Voice AI API to production.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Production Server Setup](#production-server-setup)
5. [Cloud Deployment](#cloud-deployment)
6. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Pre-Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with all required variables
- [ ] OpenRouter API key added and tested
- [ ] Tests passing (`python test_api.py`)
- [ ] Logs configured (`LOG_LEVEL=WARNING` for production)
- [ ] Rate limiting configured
- [ ] CORS settings appropriate for your domain
- [ ] SSL certificate ready (for HTTPS)
- [ ] Database backup strategy in place (if using DB)

---

## Local Deployment

### Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run development server
python main.py
```

### Production Environment (Local)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn (4 workers)
gunicorn main:app --workers 4 --bind 0.0.0.0:5000

# Run with Gunicorn (8 workers) - for high traffic
gunicorn main:app --workers 8 --bind 0.0.0.0:5000 \
  --worker-class uvicorn.workers.UvicornWorker \
  --timeout 30
```

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create app user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run application
CMD ["gunicorn", "main:app", "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:5000", "--timeout", "30"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - DEBUG=False
      - LOG_LEVEL=INFO
      - RATE_LIMIT_REQUESTS=100
      - RATE_LIMIT_WINDOW=60
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### Build and Run Docker

```bash
# Build image
docker build -t hu-voice-ai:latest .

# Run container
docker run -d \
  --name hu-voice-api \
  -p 5000:5000 \
  -e OPENROUTER_API_KEY=your_key_here \
  -e DEBUG=False \
  hu-voice-ai:latest

# Run with docker-compose
docker-compose up -d

# Check logs
docker logs hu-voice-api

# Stop container
docker stop hu-voice-api
```

---

## Production Server Setup

### Ubuntu/Debian Server

#### 1. Initial Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
  python3.11 \
  python3.11-venv \
  python3-pip \
  nginx \
  supervisor \
  git \
  curl
```

#### 2. Create Application User

```bash
# Create user for application
sudo useradd -m -s /bin/bash huvoice

# Create app directory
sudo mkdir -p /opt/hu-voice-api
sudo chown -R huvoice:huvoice /opt/hu-voice-api
```

#### 3. Deploy Application

```bash
# Switch to app user
sudo su - huvoice

# Clone repository
cd /opt/hu-voice-api
git clone <repository_url> .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with production settings
nano .env
```

#### 4. Setup Supervisor

Create `/etc/supervisor/conf.d/hu-voice-api.conf`:

```ini
[program:hu-voice-api]
directory=/opt/hu-voice-api
command=/opt/hu-voice-api/venv/bin/gunicorn \
  main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind unix:/opt/hu-voice-api/gunicorn.sock \
  --timeout 30 \
  --access-logfile /var/log/hu-voice-api/access.log \
  --error-logfile /var/log/hu-voice-api/error.log

user=huvoice
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/hu-voice-api/supervisor.log
```

```bash
# Create log directory
sudo mkdir -p /var/log/hu-voice-api
sudo chown huvoice:huvoice /var/log/hu-voice-api

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start hu-voice-api
```

#### 5. Setup Nginx Reverse Proxy

Create `/etc/nginx/sites-available/hu-voice-api`:

```nginx
upstream hu_voice_api {
    server unix:/opt/hu-voice-api/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name api.youromain.com;
    client_max_body_size 10M;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 10M;

    # Logging
    access_log /var/log/nginx/hu-voice-api-access.log;
    error_log /var/log/nginx/hu-voice-api-error.log;

    location / {
        proxy_pass http://hu_voice_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    location /chat {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://hu_voice_api;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/hu-voice-api \
  /etc/nginx/sites-enabled/hu-voice-api

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

#### 6. Setup SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d api.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Cloud Deployment

### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. Security group: Allow 80, 443, 22
# 3. SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 4. Follow Ubuntu/Debian setup above
```

### Heroku

```bash
# 1. Create Procfile
echo "web: gunicorn main:app --worker-class uvicorn.workers.UvicornWorker" > Procfile

# 2. Create heroku app
heroku create your-app-name

# 3. Set environment variables
heroku config:set OPENROUTER_API_KEY=your_key
heroku config:set DEBUG=False

# 4. Deploy
git push heroku main
```

### Google Cloud Run

```bash
# 1. Create Dockerfile (provided above)

# 2. Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project/hu-voice-api

# 3. Deploy
gcloud run deploy hu-voice-api \
  --image gcr.io/your-project/hu-voice-api \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENROUTER_API_KEY=your_key
```

### Railway

```bash
# 1. Connect GitHub repository
# 2. Add environment variables in Railway dashboard
# 3. Deploy automatically
```

---

## Monitoring & Maintenance

### Health Monitoring

```bash
# Check application health
curl https://api.yourdomain.com/health

# Check status
curl https://api.yourdomain.com/status

# Set up automated health checks
# Option 1: Using cron
0 * * * * curl -f https://api.yourdomain.com/health || send_alert

# Option 2: Using monitoring service
# - Uptime Robot
# - PagerDuty
# - DataDog
```

### Log Management

```bash
# View application logs
sudo tail -f /var/log/hu-voice-api/error.log

# Rotate logs (add to logrotate)
/var/log/hu-voice-api/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 huvoice huvoice
    sharedscripts
    postrotate
        supervisorctl restart hu-voice-api
    endscript
}
```

### Performance Monitoring

```bash
# Monitor system resources
top -p $(pgrep -f gunicorn | head -1)

# Monitor network connections
netstat -an | grep :5000

# Monitor disk usage
df -h
du -sh /opt/hu-voice-api
```

### Backup Strategy

```bash
# Backup application
tar -czf hu-voice-api-backup-$(date +%Y%m%d).tar.gz /opt/hu-voice-api/

# Backup logs
tar -czf hu-voice-api-logs-$(date +%Y%m%d).tar.gz /var/log/hu-voice-api/

# Store backups
rsync -avz backup.tar.gz remote-server:/backup/
```

### Updates & Patches

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Update Python dependencies
cd /opt/hu-voice-api
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart service
sudo supervisorctl restart hu-voice-api
```

---

## Performance Optimization

### Gunicorn Configuration

```bash
# Calculate optimal worker count: (2 × CPU cores) + 1
# For 4-core CPU: (2 × 4) + 1 = 9 workers

gunicorn main:app \
  --workers 9 \
  --worker-class uvicorn.workers.UvicornWorker \
  --worker-connections 1000 \
  --keepalive 5 \
  --max-requests 1000 \
  --max-requests-jitter 50
```

### Nginx Caching

```nginx
# Add to nginx config
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m;

location / {
    proxy_cache api_cache;
    proxy_cache_valid 200 60m;
    proxy_cache_use_stale error timeout invalid_header updating;
    proxy_pass http://hu_voice_api;
}
```

### Redis Caching

```env
REDIS_ENABLED=True
REDIS_HOST=your-redis-host
REDIS_PORT=6379
```

---

## Security Checklist

- [ ] HTTPS enabled (SSL/TLS)
- [ ] API key not in code (use .env)
- [ ] Rate limiting configured
- [ ] CORS restricted to allowed origins
- [ ] Regular security updates
- [ ] Firewall configured
- [ ] SSH key-based authentication only
- [ ] Regular backups
- [ ] Monitoring and alerts setup
- [ ] Log analysis for suspicious activity

---

## Troubleshooting Production

### High Memory Usage

```bash
# Reduce worker count
# Reduce max_requests
# Monitor with: free -h, ps aux
```

### High CPU Usage

```bash
# Check application logs
# Profile application
# Consider upgrading instance
```

### API Key Errors

```bash
# Verify .env file loaded correctly
source /opt/hu-voice-api/.env
echo $OPENROUTER_API_KEY

# Restart application
sudo supervisorctl restart hu-voice-api
```

### Connection Issues

```bash
# Check nginx error logs
sudo tail -f /var/log/nginx/hu-voice-api-error.log

# Check firewall
sudo iptables -L

# Test connectivity
curl -v https://api.yourdomain.com/health
```

---

## Support

For deployment issues:
1. Check application logs
2. Check nginx logs
3. Check supervisor status: `sudo supervisorctl status`
4. Review configuration files
5. Test endpoints manually

---

**Document Version**: 1.0  
**Last Updated**: January 2024  
**Status**: Production Ready ✅
