# Step-by-Step Deployment Instructions

Follow these clear, step-by-step instructions to deploy the Production-Grade FastAPI Backend onto an AWS EC2 instance running Ubuntu 24.04 LTS.

---

## Step 1: Launch Ubuntu EC2 Instance
1. Log into your AWS Console and navigate to the **EC2 Dashboard**.
2. Click **Launch Instance**.
3. Name your instance (e.g., `fastapi-backend-prod`).
4. Select the official **Ubuntu Server 24.04 LTS** AMI.
5. Select instance size (minimum: `t3.micro` for testing, recommended: `t3.medium`).
6. Select or generate a new key pair (`.pem`) for SSH authentication.
7. Set storage capacity to **20 GB gp3 SSD**.

## Step 2: Configure Security Groups
Under the network settings panel of your EC2 setup, configure the following inbound firewall rules:

- **SSH (Port 22)**: Set Source to `My IP` (to secure access).
- **HTTP (Port 80)**: Set Source to `Anywhere-IPv4` (`0.0.0.0/0`).
- **HTTPS (Port 443)**: Set Source to `Anywhere-IPv4` (`0.0.0.0/0`).

## Step 3: Connect Using SSH
Locate the path to your downloaded key pair file (`.pem`), configure file permissions, and connect to your EC2 instance:
```bash
chmod 400 /path/to/your-key.pem
ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
```

## Step 4: Install Docker Engine
Execute this command block to configure dependencies, add the official GPG keys, and install Docker Engine on the server:
```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates curl gnupg

# Add Docker keyrings
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker Repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Step 5: Install Docker Compose (Non-Root Verification)
Add your SSH user to the docker group to enable passwordless container commands (requires logging out and back in to take effect):
```bash
sudo usermod -aG docker ubuntu
```

Verify that both commands are installed:
```bash
docker --version
docker compose version
```

## Step 6: Clone the Repository
Clone the application repository into `/var/www`:
```bash
sudo mkdir -p /var/www
sudo chown -R ubuntu:ubuntu /var/www
cd /var/www
git clone https://github.com/Sanket-HP/devops-fastapi-assignment.git
cd devops-fastapi-assignment
```

## Step 7: Create and Configure the `.env` File
Create a new configuration file by copying the template:
```bash
cp .env.example .env
```

Open and edit the file:
```bash
nano .env
```

Ensure the configuration variables match these settings:
```text
ENV=production
APP_NAME="Production FastAPI Backend"
POSTGRES_USER=postgres
POSTGRES_PASSWORD=generate_a_complex_password_here
POSTGRES_DB=app_db
POSTGRES_HOST=postgres
REDIS_HOST=redis
REDIS_PASSWORD=generate_another_complex_password_here
LOG_LEVEL=INFO
LOG_DIR=logs
```
*(Press `CTRL+O` and `Enter` to save, then `CTRL+X` to exit Nano)*

## Step 8: Build and Start Containers
Spin up the service stack in daemon mode:
```bash
docker compose up --build -d
```

## Step 9: Verify Running Containers
Verify that all 4 containers (`app-postgres`, `app-redis`, `app-fastapi`, `app-nginx`) are up and running:
```bash
docker compose ps
```

Verify logs for any errors:
```bash
docker compose logs -f fastapi
```

## Step 10: Verify Health Endpoint
Execute a request to the health diagnostic API:
```bash
curl http://localhost/health
```
Verify the output status displays `"status": "healthy"`.

## Step 11: Verify Swagger API Documentation
Open your local web browser and navigate to:
`http://your-ec2-public-ip/docs`

Ensure the interactive Swagger documentation loads and displays the `/users` routes.

## Step 12: Configure GitHub Actions Secrets
To enable automated deployments on repository updates, navigate to your GitHub repository under `Settings > Secrets and variables > Actions`, click **New repository secret**, and register the following variables:

1. **`SSH_HOST`**: Set to your remote AWS EC2 public IP.
2. **`SSH_USERNAME`**: Set to `ubuntu`.
3. **`SSH_PRIVATE_KEY`**: Paste the entire raw content of your private key file (`.pem`).

## Step 13: Configure GitHub Actions
Commit and push the CI/CD pipeline code. The workflow is already created at `.github/workflows/deploy.yml` and triggers automatically on commits to the `main` or `master` branches.

## Step 14: Test Automatic Deployment
Make a minor cosmetic adjustment or comment modification to your code, then commit and push to Git:
```bash
git add .
git commit -m "chore: test automatic deployment pipeline"
git push origin main
```

## Step 15: Verify Successful Deployment
1. Navigate to the **Actions** tab inside your GitHub repository.
2. Monitor the active deployment run.
3. Ensure both the **Lint & Verify Build** and **Deploy to Production VPS** jobs execute successfully.

## Step 16: Troubleshooting
- **Database Connection Error**:
  Ensure `POSTGRES_HOST=postgres` inside `.env` instead of `localhost`.
- **Log permissions errors**:
  If the FastAPI container fails because of log folder write permissions:
  ```bash
  sudo chown -R 10001:10001 /var/lib/docker/volumes/devops-fastapi-assignment_app_logs/_data
  ```
- **Redis access errors**:
  Ensure `REDIS_PASSWORD` inside `.env` matches the configuration and that the application host points to `redis`.
