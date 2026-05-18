# Microservices App

Three independent FastAPI services wired together:

```
Browser → API Gateway (:8000) → Frontend (:3000)  (serves HTML)
                              → Hello Service (:5000)  (business logic)
```

## Project Structure

```
microservices/
├── services/
│   ├── api-gateway/      # Routes all traffic
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── frontend/         # Serves the HTML home page
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── hello-service/    # Business logic API
│       ├── main.py
│       ├── requirements.txt
│       └── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
└── k8s/
    ├── namespace.yaml
    ├── deployments.yaml
    ├── services.yaml
    └── ingress.yaml
```

---

## Step 1 — Run locally with Docker Compose

```bash
# Build and start all three services
docker compose up --build

# Open in browser
open http://localhost:8000

# Check all service health
curl http://localhost:8000/health

# Call the API directly
curl "http://localhost:8000/api/hello?name=Alice"
```

---

## Step 2 — Push to GitHub

```bash
git init
git add .
git commit -m "feat: microservices app"
git remote add origin https://github.com/YOUR_ORG/YOUR_REPO.git
git push -u origin main
```

---

## Step 3 — GitHub Actions (automatic)

The workflow in `.github/workflows/ci.yml` triggers on every push to `main` and:
1. Builds all three Docker images in parallel
2. Pushes them to GitHub Container Registry (GHCR) — free, no extra setup
3. Deploys to Kubernetes using `kubectl apply`

### Required GitHub Secrets

Go to **Settings → Secrets → Actions** and add:

| Secret | Value |
|--------|-------|
| `KUBECONFIG` | `base64 -i ~/.kube/config` output |

Images are auto-tagged with `latest` and the commit SHA.

---

## Step 4 — Kubernetes

### Prerequisites
- A running cluster (EKS, GKE, AKS, or local minikube/k3s)
- `kubectl` pointing at it
- NGINX Ingress Controller installed

### One-time setup

```bash
# Replace YOUR_ORG in k8s/deployments.yaml with your GitHub username/org
sed -i 's/YOUR_ORG/mygithubuser/g' k8s/deployments.yaml

# Deploy everything
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/

# Watch pods come up
kubectl get pods -n microservices -w
```

### Verify

```bash
# All pods should be Running
kubectl get pods -n microservices

# Check services
kubectl get svc -n microservices

# Port-forward the gateway locally if no ingress yet
kubectl port-forward svc/api-gateway-svc 8000:80 -n microservices
open http://localhost:8000
```

### Update domain

Edit `k8s/ingress.yaml` and replace `myapp.example.com` with your real domain,
then point your DNS A record to the ingress controller's external IP:

```bash
kubectl get svc -n ingress-nginx   # copy EXTERNAL-IP
```

---

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Home page (HTML) |
| `GET /api/hello?name=Alice` | Hello API → returns JSON |
| `GET /health` | Gateway health + dependency check |
