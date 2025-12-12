# CI/CD Deployment Documentation

## Overview

This project implements a complete CI/CD pipeline with GitHub Actions that:
1. ✅ Runs comprehensive unit and integration tests
2. ✅ Performs security scanning with Trivy
3. ✅ Builds and pushes Docker image to Docker Hub
4. ✅ Supports multi-platform builds (amd64, arm64)

## Workflow Architecture

### 1. **Test Job** (Runs on: Ubuntu Latest)
- **PostgreSQL Service**: Provides test database with health checks
- **Steps**:
  - Checkout code
  - Setup Python 3.10
  - Cache pip dependencies
  - Install requirements and Playwright
  - Run unit tests (no DB required)
  - Run integration tests (with PostgreSQL)
  - Run e2e tests (if they exist)

**Environment Variables**:
- `DATABASE_URL`: `postgresql://user:password@localhost:5432/mytestdb`

### 2. **Security Job** (Depends on: test)
- **Trivy Vulnerability Scanner**: Scans Docker image for security issues
- **Failure Conditions**: Fails on CRITICAL or HIGH severity vulnerabilities
- **Output**: Table format report

### 3. **Deploy Job** (Depends on: security)
- **Conditions**: Only runs on pushes to `main` branch
- **Docker Operations**:
  - Login to Docker Hub
  - Build image for multiple platforms (linux/amd64, linux/arm64)
  - Push with tags:
    - `${DOCKERHUB_USERNAME}/is218-module10:latest`
    - `${DOCKERHUB_USERNAME}/is218-module10:${GIT_SHA}`
  - Enable caching for faster builds

## Setup Instructions

### 1. Configure GitHub Secrets

Add these secrets to your GitHub repository:

1. Go to **Settings → Secrets and variables → Actions**
2. Create the following secrets:

| Secret Name | Value | Description |
|---|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username | Used for login and image tagging |
| `DOCKERHUB_TOKEN` | Your Docker Hub access token | Create at https://hub.docker.com/settings/security |

**To create Docker Hub Token**:
1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Give it a name (e.g., "GitHub Actions")
4. Set permissions (recommend "Read & Write")
5. Copy the token and save as GitHub Secret

### 2. Verify Workflow Configuration

The workflow file is located at: `.github/workflows/test.yml`

Key configuration points:
- Triggers: `push` to `main` and `pull_request` to `main`
- Python version: 3.10
- PostgreSQL version: latest
- Docker tags use `${DOCKERHUB_USERNAME}` from secrets

## Running the Pipeline

### Manual Trigger (Optional)

To manually trigger the workflow:
```bash
git push origin main
```

The workflow will automatically:
1. Run all tests
2. Perform security scan
3. Build Docker image
4. Push to Docker Hub (if on main branch and all checks pass)

### Monitoring Workflow Execution

1. Go to **Actions** tab in your GitHub repository
2. Select the workflow run
3. View logs for each job:
   - **test**: Python test execution logs
   - **security**: Trivy scan results
   - **deploy**: Docker build and push logs

## Test Configuration

### Unit Tests
- Location: `tests/unit/`
- No database required
- Coverage report: Generated with `--cov=app`
- Report format: JUnit XML

### Integration Tests
- Location: `tests/integration/`
- Requires PostgreSQL service
- Database credentials from `DATABASE_URL` env var
- Tests user model, authentication, validation

### Test Execution

```bash
# Run all tests locally
pytest tests/ -v --cov=app

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Generate coverage report
pytest --cov=app --cov-report=html
```

## Docker Image Build

### Local Build
```bash
docker build -t is218-module10:latest .
```

### Push to Docker Hub
```bash
# Login
docker login -u your_username -p your_token

# Tag image
docker tag is218-module10:latest your_username/is218-module10:latest

# Push
docker push your_username/is218-module10:latest
```

### Running Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:password@host:5432/db" \
  your_username/is218-module10:latest
```

## Workflow Status

View the workflow status badge in your GitHub Actions:
- Navigate to **Actions** tab
- Select the workflow
- Copy the status badge markdown if available

## Troubleshooting

### Tests Fail Locally But Pass in GitHub Actions

**Cause**: Database URL mismatch
**Solution**: 
```bash
# Set environment variable
export DATABASE_URL="postgresql://user:password@localhost:5432/mytestdb"
```

### Docker Build Fails

**Possible Issues**:
1. Missing Dockerfile
2. Python version mismatch
3. Dependency installation failure

**Debug**:
```bash
docker build -t test:debug . --progress=plain
```

### Docker Hub Push Fails

**Possible Issues**:
1. Invalid Docker Hub credentials
2. Token expired
3. Repository doesn't exist

**Solution**:
1. Verify secrets in GitHub
2. Regenerate Docker Hub token
3. Ensure repository is public or private (configure access)

## Continuous Improvement

### Monitor Build Times
- GitHub Actions provides build duration logs
- Optimize by:
  - Using cached layers in Docker
  - Parallel test execution
  - Using smaller base images

### Security Scanning
- Trivy is configured to fail on HIGH/CRITICAL vulnerabilities
- Review and update dependencies regularly
- Keep Python and system packages updated

### Docker Image Optimization
- Current: Python 3.10-slim (more optimized than full image)
- Multi-platform builds ensure compatibility

## Files Modified

- `.github/workflows/test.yml`: Updated test commands and Docker Hub credentials
- `requirements.txt`: All dependencies declared
- `Dockerfile`: Production-ready image with health checks
- `main.py`: FastAPI entry point

## Next Steps

1. ✅ Add Docker Hub secrets to GitHub
2. ✅ Commit and push changes to main branch
3. ✅ Monitor the GitHub Actions workflow
4. ✅ Verify Docker image appears on Docker Hub
5. ✅ Test pulling and running the image locally

---

**Workflow Diagram**:
```
Code Push to Main
    ↓
GitHub Actions Triggered
    ↓
[Test Job] - Run Tests with PostgreSQL
    ↓
[Security Job] - Trivy Scan Docker Image
    ↓
[Deploy Job] - Push to Docker Hub
    ↓
✅ Pipeline Complete (or ❌ Failed)
```
