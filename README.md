# Production-Grade FastAPI Backend with Docker, PostgreSQL, Redis, NGINX & GitHub Actions CI/CD

A high-performance, battle-tested, and production-ready FastAPI blueprint engineered for enterprise-grade performance, scalability, and security. This deployment architecture is fully optimized for containerized isolation, structured monitoring, automated pipeline delivery, and cloud hosting on AWS EC2 running Ubuntu 24.04 LTS.

## 📌 Project Overview

This repository demonstrates the deployment of a highly scalable, production-ready FastAPI application configured inside a tightly decoupled Docker container network. Every architectural component of this setup is hardened, streamlined, and ready for commercial environments:

> [!NOTE]
> **Key Architecture Highlights:**
>
> - **NGINX Reverse Proxy**: Fronts incoming web traffic, handles SSL termination, manages payload restrictions, mitigates clickjacking/XSS vectors, and optimizes resource distribution using client-side caching and standard Gzip compression.
> - **FastAPI Core**: A Python 3.12 asynchronous web frame implementing type-safe settings parsing, modern endpoints design, modular dependency injection, and centralized log structuring.
> - **PostgreSQL Persistence Engine**: Reliable database architecture configured with custom operational metrics, SQLAlchemy 2.0 transaction pools, and automated database extractions.
> - **Redis Cache Layer**: Low-latency query engine designed to dramatically accelerate database query returns, coupled with programmatic write-through cache invalidation.
> - **GitHub Actions Infrastructure**: Seamless continuous integration and deployment pipeline verifying system constraints, building images, and performing SSH rolling deployments onto target remote clouds.

## 🏗️ Architecture Diagrams

### 1. Unified CI/CD & Cloud Infrastructure Pipeline

This flowchart illustrates the continuous integration pipeline executing locally, communicating with GitHub Actions, compiling system constraints, and executing automated GitOps delivery to AWS Cloud infrastructure.

```mermaid
flowchart TD
    A[GitHub Repository] -->|Push/PR to main| B[GitHub Actions]
    B -->|SSH Deployment Keys| C[AWS EC2 Ubuntu]
    C -->|Orchestrated via| D[Docker Compose]
    D -->|Exposes Public HTTP| E[NGINX]
    E -->|Forwards to Port 8000| F[FastAPI]
    F -->|Connection Pool| G[(PostgreSQL)]
    F -->|Query Cache| H[(Redis)]
```

### 2. Request Lifecycle & Routing Architecture

This diagram traces individual HTTP payloads entering through NGINX and getting parsed down through routing networks, caching pools, and transactional databases.

```mermaid
flowchart TD
    Client[Internet / Client] -->|Port 80/443| Nginx[NGINX Reverse Proxy]
    Nginx -->|Upstream Reverse Proxy| FastAPI[FastAPI Application]
    FastAPI -->|Key-Value Store / Cache| Redis[(Redis Cache)]
    FastAPI -->|Relational Database| Postgres[(PostgreSQL DB)]
```

## ⚙️ Features

- **Pydantic Config Core**: Strictly validated setting imports using `pydantic-settings` to enforce type safety on environment file loads, ensuring incorrect variable shapes fail during early system startup.
- **SQLAlchemy 2.0 Connection Pool**: Deeply optimized ORM database engine setup with active query recycling, proactive pre-ping connectivity verifications, and custom overflow transaction buffers.
- **Redis-Powered Cache Layer**: High-speed, key-value execution caching critical user search queries. Configured with automated logic ensuring stale cache invalidation when data updates occur.
- **Comprehensive Health Testing**: Dedicated diagnostical `/health` endpoint analyzing database connection state and Redis responsiveness, returning real-time status payloads (`200 OK`, `degraded`, or `503 Service Unavailable`).
- **Structured File and Console Logging**: High-visibility diagnostics separating general operations from critical execution exceptions using automated standard stdout logs alongside isolated tracking logs.
- **Hardened NGINX Gateway**: Optimized configuration featuring reverse proxy routing, customizable body size guardrails, Gzip optimizations, and reliable response security headers (`HSTS`, `CSP`, `XSS-Protection`).
- **Production Multi-Stage Dockerfile**: Highly optimized multi-stage build footprint excluding compilation SDKs from deployment artifacts, running as a secure, unprivileged system user (`appuser`, UID: 10001).
- **Automated Backup and Restore Routines**: Robust database archiving workflows that generate compressed backups, enforce automated rotations, and facilitate straightforward recovery commands.

## 📁 Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD automated deployment workflow
├── app/
│   ├── api/
│   │   ├── deps.py             # Database sessions and Redis client injection dependencies
│   │   └── v1/
│   │       ├── router.py       # Aggregate API router pattern incorporating endpoints
│   │       └── endpoints/
│   │           ├── health.py   # Diagnostics and microservices health checking endpoints
│   │           └── users.py    # Clean CRUD operations supporting CRUD cache invalidation
│   ├── core/
│   │   ├── config.py           # Strictly typed config settings powered by Pydantic V2
│   │   └── logging.py          # Modular, high-output console and file logger configuration
│   ├── database/
│   │   ├── base.py             # Global class declarations and metadata references
│   │   └── session.py          # Relational engine initialization and connection pool configuration
│   ├── models/
│   │   └── user.py             # Database scheme and structural user model mapping
│   ├── schemas/
│   │   └── user.py             # Type-safe input and serialization validation via Pydantic
│   ├── services/
│   │   └── cache.py            # Optimized Redis key-value cache operations layer
│   └── main.py                 # FastAPI application instantiation, hooks, and routing setup
├── nginx/
│   ├── Dockerfile              # Standard, lightweight production proxy image configuration
│   └── nginx.conf              # Production-grade proxy gateway routing and security definitions
├── scripts/
│   └── backup.sh               # Executable engine data dump, gzip, and rotational automation
├── Dockerfile                  # Secure, multi-stage optimized Python image creation file
├── docker-compose.yml          # Container configuration for production stack services
├── requirements.txt            # Explicit dependency pinning tracking external python packages
└── .env.example                # Deployment variable template with secure default placeholders
```

## 🚀 Installation & Local Execution

Follow these steps to run a fully functional, containerized development environment on your local workstation:

### 1. Clone the Repository

```bash
git clone https://github.com/Sanket-HP/devops-fastapi-assignment.git
cd devops-fastapi-assignment
```

### 2. Configure Local Settings

Initialize your local runtime variables:

```bash
cp .env.example .env
```

> [!IMPORTANT]
> Always open `.env` and configure custom database passwords, safe credentials, and host parameters before spinning up your container infrastructure.

### 3. Launch Services with Docker Compose

```bash
docker compose up --build -d
```

### 4. Verify Active Runtimes

Verify that all services are fully running and error-free:

```bash
docker compose ps
```

### 5. Inspect Container Logging Outputs

Check execution traces across the multi-container stack:

```bash
docker compose logs -f
```

## ☁️ Production Deployment (AWS EC2 Ubuntu 24.04 LTS)

Follow these cloud configuration procedures to deploy the stack onto a clean AWS EC2 instance:

### 1. Provision EC2 Host Infrastructure

1. Launch an AWS EC2 Instance utilizing the official Ubuntu Server 24.04 LTS AMI.
2. Select an instance size tailored for your traffic demands (e.g., `t3.medium` or higher for small production workloads).
3. Open ports in your AWS Security Group to allow necessary ingress traffic:
   - **Port 22**: Restricted to your trusted IP address (SSH Management).
   - **Port 80**: Open globally `0.0.0.0/0` (HTTP web requests).
   - **Port 443**: Open globally `0.0.0.0/0` (Secure HTTPS transactions).

### 2. Remote Machine Provisioning

Establish an SSH connection with your remote server:

```bash
ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
```

Update system packages and install prerequisites:

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install git curl -y
```

### 3. Install Docker Engine & Compose

Install Docker CE on your remote host machine:

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install Docker packages:
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

Verify that Docker is active and system startup services are running:

```bash
sudo systemctl enable docker
sudo systemctl status docker
```

Configure non-root Docker execution permissions (optional but highly recommended):

```bash
sudo usermod -aG docker ubuntu
# Log out and log back in to apply group membership changes
```

### 4. Deploy Application Environment

Clone the source code on your remote server and set up configurations:

```bash
cd /var/www
sudo chown -R ubuntu:ubuntu /var/www
git clone https://github.com/Sanket-HP/devops-fastapi-assignment.git
cd devops-fastapi-assignment

# Build env configurations
cp .env.example .env
```

> [!WARNING]
> Ensure `POSTGRES_HOST` in `.env` points to the internal database service container `postgres` rather than `localhost` to allow correct inter-container resolution.

Build and run your production cluster:

```bash
docker compose -f docker-compose.yml up --build -d
```

## 🔄 GitHub Actions CI/CD Pipeline

This project implements GitOps principles using a fully automated continuous integration and continuous deployment pipeline via GitHub Actions.

```mermaid
flowchart LR
    Push[Code Push] --> Test[Lint / Test]
    Test --> Build[Docker Dry Build]
    Build --> SSH[SSH to AWS EC2]
    SSH --> Pull[Git Pull Changes]
    Pull --> Up[Compose Up --build]
    Up --> Health[Endpoint Health Check]
```

### Pipeline Sequence Explanation

1. **Repository Checkout**: Clones code changes onto the GitHub execution container environment.
2. **Setup Python Environment**: Configures the runner node to match Python 3.12 requirements.
3. **Automated Linting (Ruff)**: Performs static analysis validation, checking for syntactic compliance and enforcing optimal standards.
4. **Dry Docker Build Check**: Verifies that your core Dockerfile builds without compilation errors before deploying to the server.
5. **Establish SSH Connection**: Securely connects to your remote AWS EC2 host using SSH keys stored in GitHub Secrets.
6. **Git Synchronization**: Triggers a fast-forward git pull of the target branch directly on the hosting instance.
7. **Compose Stack Rebuild**: Executes a rolling update (`docker compose up --build -d`) to deploy updated container images with minimal disruption.
8. **Automated Health Check**: Hits the `/health` endpoint on the deployed instance to ensure the stack is healthy before marking the deployment as successful.

### Required Secrets Configuration

To enable CI/CD automation, navigate to your repository settings under `Settings > Secrets and variables > Actions` and register the following secrets:

| Secret Key Name | Expected Value |
|---|---|
| `SSH_HOST` | The public DNS name or IPv4 address of your remote AWS EC2 host. |
| `SSH_USERNAME` | The deployment user account assigned by your cloud provider (typically `ubuntu`). |
| `SSH_PRIVATE_KEY` | The raw contents of the private key (`.pem`) used to authorize the SSH connection. |

## 🎛️ Environment Variables Reference

Adjust settings within the `.env` configuration file to configure different runtime environments:

| System Environment Key | Expected Input Type | Default Fallback Value | Functional Role |
|---|---|---|---|
| `ENV` | `string` | `production` | Active deployment environment context (`development` or `production`). |
| `APP_NAME` | `string` | `FastAPI Backend` | Global identifier display value surfaced in application headers and logs. |
| `POSTGRES_USER` | `string` | `postgres` | Administrative user account credentials matching the PostgreSQL database engine. |
| `POSTGRES_PASSWORD` | `string` | `postgres` | Cryptographically complex user login string safeguarding the PostgreSQL DB. |
| `POSTGRES_DB` | `string` | `app_db` | Targets the specific datastore instance for the backend ORM's active schemas. |
| `POSTGRES_HOST` | `string` | `localhost` | Identifies the network host database location (`postgres` inside compose networks). |
| `REDIS_HOST` | `string` | `localhost` | Access address of your Redis cluster (`redis` for internal compose access). |
| `REDIS_PASSWORD` | `string` | `None` | Authentication string required to access your caching database instance. |
| `LOG_LEVEL` | `string` | `INFO` | Filtering granularity for output logs (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). |
| `LOG_DIR` | `string` | `logs` | Physical directory storage path designated for housing system log files. |

## 📖 API Documentation

Once your deployment finishes spinning up, you can review, execute, and interact with the dynamic Open-API specification via Swagger at `http://<YOUR_HOST_ADDRESS>/docs` or Redocly at `http://<YOUR_HOST_ADDRESS>/redoc`.

### Utility & Core System Operations

| Method | Endpoint Route | Request Headers | Response Structure | Functional Role |
|---|---|---|---|---|
| `GET` | `/` | Standard | JSON Object | Endpoint routing check that returns identity metadata. |
| `GET` | `/health` | Standard | Diagnostics JSON | Verifies live state connections for both PostgreSQL and Redis cache engines. |

### User Management Actions

| Method | Endpoint Route | Payloads Allowed | Cache Behavioral Impact | Functional Role |
|---|---|---|---|---|
| `GET` | `/users` | Pagination Params | Pulls from Cache, DB Fallback | Retrieves page list of registered users. |
| `GET` | `/users/{id}` | Path Parameter ID | Direct DB Fetch | Inspects profiles for a unique user record. |
| `POST` | `/users` | User Schema Model | Invalidates User Cache | Creates a new user record. |
| `PUT` | `/users/{id}` | Update Schema Model | Invalidates User Cache | Updates details of a registered user. |
| `DELETE` | `/users/{id}` | Path Parameter ID | Invalidates User Cache | Removes a registered user from the database. |

## 🏥 Automated Health Checks

The system implements a thorough multi-service monitoring pattern under the `/health` path. It executes actual database query tests and Redis connection checks on every call to verify backend integrity rather than returning a static mock response.

### 1. Healthy State Payload (Status: 200 OK)

```json
{
  "status": "healthy",
  "timestamp": "2026-07-02T11:45:00.000000",
  "checks": {
    "database": {
      "status": "connected",
      "latency_ms": 1.42
    },
    "redis": {
      "status": "connected",
      "latency_ms": 0.89
    }
  }
}
```

### 2. Degraded State Payload (Status: 503 Service Unavailable)

```json
{
  "status": "degraded",
  "timestamp": "2026-07-02T11:46:12.110200",
  "checks": {
    "database": {
      "status": "connected",
      "latency_ms": 2.10
    },
    "redis": {
      "status": "disconnected",
      "error": "Timeout accessing socket connection parameters"
    }
  }
}
```

## 📝 Logging Strategy

The backend application implements a two-tier structured logging setup, outputting messages to both standard output (stdout) and persistent volume-mounted directories.

Host System Log Mount Path:
`/var/lib/docker/volumes/devops-fastapi-assignment_app_logs/_data/`
- `app.log`: Dynamic production operational tracking (retains 5 history archives at 10MB)
- `error.log`: High-priority exception handler log capturing occurrences of `ERROR` / `CRITICAL` level

### Log Configuration Properties

- **Format Layout**: Formatted structured parameters capturing precise timestamps, origin module files, execution lines, logging categories, and the payload message.
- **Consolidated Log Rotation**: Built-in Python handlers capture size bounds per active log file. Files automatically roll over at 10MB, keeping a history of up to 5 standard backup iterations.

## 💾 Database Backup & Recovery

Keep your data secure by scheduling automated database backups using the lightweight shell backup engine.

### 1. Enable Automated Cron Executions

First, ensure your automation script is executable:

```bash
chmod +x scripts/backup.sh
```

Register a custom Cron utility operation in your server environment:

```bash
crontab -e
```

Insert this entry at the bottom of the crontab configuration to trigger a backup extraction daily at 2:00 AM:

```text
0 2 * * * /bin/bash /var/www/devops-fastapi-assignment/scripts/backup.sh >> /var/log/cron-backup.log 2>&1
```

### 2. Database Restoration Protocol

Restore a compressed Gzipped SQL database backup using this decompression stream:

```bash
gunzip -c /var/backups/postgres/app_db_backup_2026-07-02_020000.sql.gz | docker exec -i postgres psql -U postgres -d app_db
```

## 🔒 Enterprise Security & Server Hardening

Before deploying your containers to production on AWS, implement the following server hardening security practices:

### 1. Run Docker Containers as Non-Root Users

The core API image is structured with explicit non-root operational standards:

```dockerfile
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser
USER appuser
```

This isolates filesystem operations, mitigating container escape vulnerabilities.

### 2. Configure Host Firewalls (UFW)

Establish tight host access limits using the Uncomplicated Firewall (UFW):

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp     # Limit access to verified trusted IPs where possible
sudo ufw allow 80/tcp     # HTTP connection channel
sudo ufw allow 443/tcp    # HTTPS secure connection channel
sudo ufw enable
```

### 3. Hardening SSH Configuration

Restrict remote shell logins on your host machine. Edit `/etc/ssh/sshd_config`:

```text
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
```

Reload your daemon processes to apply these changes:

```bash
sudo systemctl restart sshd
```

### 4. Mitigate Automated Attacks with Fail2Ban

Prevent brute-force scanning attempts:

```bash
sudo apt-get install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 5. Configured NGINX Security Headers

The built-in proxy server configuration is hardened with the following active response headers:

```nginx
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## 🌐 SSL Termination Configuration (Let's Encrypt / Certbot)

By default, this server setup handles traffic over standard HTTP because it is initially deployed on AWS EC2 using a temporary Public IP address. In real-world production environments, you should map your instance to a public domain name and install Let's Encrypt SSL certificates.

### Production SSL Setup Steps (Using Certbot on the Host Host Machine)

If you run NGINX directly on your host to route traffic to the container network, use Certbot to automate SSL certificates:

```bash
# Install Certbot and Nginx plugins on the host machine
sudo apt-get install certbot python3-certbot-nginx -y

# Request and configure your SSL certificates automatically
sudo certbot --nginx -d api.yourdomain.com
```

### Alternative: Secure In-Docker Mounting

To keep your NGINX proxy containerized while supporting SSL, mount your host's SSL certificate directories directly into your Compose containers:

```yaml
# docker-compose.yml volume updates for NGINX:
volumes:
  - /etc/letsencrypt:/etc/letsencrypt:ro
  - /var/lib/letsencrypt:/var/lib/letsencrypt:ro
```

Update `nginx/nginx.conf` to direct incoming traffic through secure standard SSL channels:

```nginx
server {
    listen 443 ssl;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://fastapi:8000;
        # ...
    }
}
```

> [!TIP]
> Certbot automates certificate renewals through cron jobs on the host. These updates are reflected in your containers instantly because your `/etc/letsencrypt` folder is mounted as a read-only live volume.

## 🔬 Operational Verification

Verify your production deployment using these standard operational commands:

### 1. Analyze Container Processes

```bash
docker compose ps
```

Expected Output:

```text
NAME                IMAGE                               COMMAND                  SERVICE             CREATED             STATUS              PORTS
app-nginx           devops-fastapi-assignment-nginx     "/docker-entrypoint.…"   nginx               10 minutes ago      Up 10 minutes       0.0.0.0:80->80/tcp
app-fastapi         devops-fastapi-assignment-fastapi   "uvicorn app.main:ap…"   fastapi             10 minutes ago      Up 10 minutes       8000/tcp
app-postgres        postgres:16-alpine                  "docker-entrypoint.s…"   postgres            10 minutes ago      Up 10 minutes       5432/tcp
app-redis           redis:7-alpine                      "docker-entrypoint.s…"   redis               10 minutes ago      Up 10 minutes       6379/tcp
```

### 2. Verify System Response Streams

Check the core web entry routes:

```bash
curl -I http://<EC2_PUBLIC_IP>/
```

Check the health checking diagnostics API:

```bash
curl http://<EC2_PUBLIC_IP>/health
```

## 🛠️ Troubleshooting

### Docker Compose Networking Obstacles

- **Symptom**: `sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) Could not translate host name "postgres"`
- **Fix**: Verify that you are referencing the correct service network alias defined in your `docker-compose.yml` (`postgres`), rather than using `localhost` or `127.0.0.1` inside your `.env` configuration.

### Redis Cache Host Connection Refusal

- **Symptom**: Connection timeout/refusal during service health inspections.
- **Fix**: Verify that Redis is active and verify its configuration parameters:
  ```bash
  docker compose logs redis
  ```
  If Redis password security is active on the container, ensure your `.env` file lists matching credentials under `REDIS_PASSWORD`.

### Log Folder File System Permissions

- **Symptom**: Container crashes during initialization or throws system permission errors when attempting to write logs to disk.
- **Fix**: Verify that your host volume storage directory matches the unprivileged runtime system user's configurations (`appuser`, UID: 10001):
  ```bash
  sudo chown -R 10001:10001 /var/lib/docker/volumes/devops-fastapi-assignment_app_logs/_data
  ```

### GitHub Actions Deployment Pipeline Disruptions

- **Symptom**: SSH execution timeouts or permission denied errors.
- **Fix**:
  - Verify that your `SSH_PRIVATE_KEY` secret contains your raw private key in its entirety (including the `-----BEGIN OPENSSH PRIVATE KEY-----` header and footer lines).
  - Ensure your AWS EC2 Security Group rules permit SSH ingress traffic from GitHub's runner IP blocks, or keep port 22 open globally if you don't restrict IP access.

## 📈 Future Architecture Roadmap

To scale this deployment further, consider the following enhancements:

1. **Kubernetes (EKS) Orchestration**: Migrate Docker Compose structures to unified Helm chart blueprints to support automated horizontal pod scaling (HPA).
2. **Infrastructure as Code (IaC)**: Automate the deployment of AWS resources (EC2, VPCs, and Security Groups) using custom Terraform scripts.
3. **Prometheus & Grafana Observability**: Integrate metric exporters to gather real-time application and resource telemetry.
4. **Application Load Balancer Integration**: Front NGINX servers with an AWS Application Load Balancer to offload SSL processing.
5. **Blue-Green Deployment Pipelines**: Configure advanced CD routes to deploy new application versions with zero downtime.
