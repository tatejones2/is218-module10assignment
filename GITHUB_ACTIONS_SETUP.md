# GitHub Actions Setup Guide

## Quick Start for CI/CD Deployment

### Step 1: Create Docker Hub Access Token

1. Go to https://hub.docker.com/settings/security
2. Click **"New Access Token"**
3. Enter token name: `GitHub Actions`
4. Select permissions: **Read & Write**
5. Click **Generate**
6. **IMPORTANT**: Copy the token immediately (you won't see it again)

### Step 2: Add GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Add the following secrets:

#### Secret 1: DOCKERHUB_USERNAME
- **Name**: `DOCKERHUB_USERNAME`
- **Value**: Your Docker Hub username (e.g., `tatejones2`)
- Click **Add secret**

#### Secret 2: DOCKERHUB_TOKEN
- **Name**: `DOCKERHUB_TOKEN`
- **Value**: Paste the token you generated in Step 1
- Click **Add secret**

### Step 3: Create Public Repository on Docker Hub (Optional but Recommended)

1. Go to https://hub.docker.com/
2. Click **Create Repository**
3. Name: `is218-module10`
4. Visibility: Public (recommended for portfolio)
5. Click **Create**

### Step 4: Verify Setup

1. Commit and push a change to `main` branch:
```bash
git add DEPLOYMENT.md
git commit -m "Initial setup"
git push origin main
```

2. Go to GitHub repository **Actions** tab
3. Watch the workflow execute:
   - ✅ **test** job runs tests with PostgreSQL
   - ✅ **security** job scans Docker image
   - ✅ **deploy** job pushes to Docker Hub

### Step 5: Monitor Deployment

**In GitHub**:
- Actions tab shows build status
- Click workflow run to see detailed logs

**In Docker Hub**:
- Go to https://hub.docker.com/r/your_username/is218-module10
- Verify image tags appear:
  - `latest` (most recent)
  - `<git_sha>` (specific commit version)

## Troubleshooting

### Issue: "Authentication failed when pushing image"

**Solution**: 
1. Verify `DOCKERHUB_USERNAME` secret is correct
2. Verify `DOCKERHUB_TOKEN` is NOT expired
3. Regenerate token if expired
4. Check secrets are visible in workflow logs (they should be masked)

### Issue: "Test failed in GitHub Actions but passes locally"

**Possible causes**:
- DATABASE_URL environment variable not set in Actions
- Python version mismatch (3.10 required)
- PostgreSQL service not ready

**Solution**: Check workflow logs and verify PostgreSQL health check passes

### Issue: "Docker image push skipped"

**Possible causes**:
- Changes pushed to branch other than `main`
- Security scan failed

**Solution**: 
- Push only to `main` for deployment
- Fix security issues flagged by Trivy

## Testing Locally Before Pushing

```bash
# Run tests locally
pytest tests/ -v --cov=app

# Build Docker image locally
docker build -t is218-module10:test .

# Run security scan locally
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image is218-module10:test
```

## Viewing Workflow Logs

1. Go to **Actions** tab
2. Click the workflow run
3. Click the job (test, security, or deploy)
4. Expand any step to see logs
5. Search for errors or important information

## Next Steps

- ✅ Setup secrets in GitHub
- ✅ Push changes to trigger workflow
- ✅ Monitor first deployment
- ✅ Pull image from Docker Hub: `docker pull your_username/is218-module10:latest`
- ✅ Test running the container locally
- ✅ Add workflow status badge to README

---

**Questions?** Check the [DEPLOYMENT.md](DEPLOYMENT.md) for detailed documentation.
