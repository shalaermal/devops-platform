# DevOps Platform

A production-grade DevOps platform built on Kubernetes, simulating real-world company infrastructure. This project covers the full lifecycle of modern cloud infrastructure — from provisioning to deployment, monitoring, and automated operations.

---

## Architecture Overview

```
GitHub (Source of Truth)
        |
        |-- Push to main
        |
GitHub Actions (CI/CD)
        |
        |-- Build & Push Docker Images
        |-- ECR (AWS Container Registry)
        |
ArgoCD (GitOps)
        |
        |-- Sync to Kubernetes Cluster
        |
Kind Cluster (Local Kubernetes)
        |
        |-- ingress-nginx (Traffic Management)
        |-- podinfo (Demo Workload)
        |-- Prometheus (Metrics Collection)
        |-- Grafana (Metrics Visualization)
        |-- Loki (Log Aggregation)
        |-- AlertManager (Alerting)
        |-- HPA (Auto Scaling)
        |-- CronJobs (Scheduled Tasks)
        |
AWS (Cloud Infrastructure)
        |-- S3 (Storage & Artifacts)
        |-- ECR (Container Registry)
        |-- IAM + OIDC (Secure Authentication)
```

---

## Stack

| Category | Technology |
|---|---|
| Cloud | AWS (S3, ECR, IAM) |
| Infrastructure as Code | Terraform |
| Container Orchestration | Kubernetes (kind) |
| CI/CD | GitHub Actions |
| GitOps | ArgoCD |
| Monitoring | Prometheus + Grafana |
| Logging | Loki + Promtail |
| Alerting | AlertManager |
| Load Testing | k6 |
| Traffic Management | ingress-nginx + MetalLB |
| Auto Scaling | HPA + metrics-server |
| Scheduled Jobs | Kubernetes CronJobs |
| Containerization | Docker |

---

## Project Structure

```
devops-platform/
├── .github/
│   └── workflows/
│       ├── ci.yaml              # CI Pipeline (runs on PR)
│       └── cd.yaml              # CD Pipeline (runs on merge to main)
├── apps/
│   ├── frontend/                # React application
│   ├── api/                     # Python FastAPI
│   └── worker/                  # Python background worker
├── kubernetes/
│   ├── apps/
│   │   └── podinfo/             # Demo workload manifests
│   ├── cronjobs/                # Scheduled job definitions
│   ├── ingress-nginx/           # Ingress controller values
│   ├── loki/                    # Logging stack values
│   ├── monitoring/              # Prometheus + Grafana values
│   └── podinfo/                 # Demo workload Helm values
├── k6/
│   └── load-test.js             # Load testing scripts
├── scripts/
│   └── start-services.sh        # Local development helper
├── terraform/
│   ├── environments/
│   │   └── dev/                 # Dev environment configuration
│   └── modules/
│       ├── ecr/                 # ECR repositories module
│       ├── iam/                 # IAM roles and policies module
│       ├── kind/                # Kind cluster module
│       └── s3/                  # S3 bucket module
└── docs/
    └── runbooks/                # Operational runbooks
```

---

## Infrastructure

### AWS (Terraform)

All AWS resources are provisioned and managed with Terraform using a modular structure.

**S3** — stores Terraform state and build artifacts. Configured with versioning and AES256 server-side encryption.

**ECR** — private container registry for Docker images. Three repositories are provisioned: `frontend`, `api`, and `worker`. Each repository has a lifecycle policy that retains only the 10 most recent images and automatically scans images on push for vulnerabilities.

**IAM** — GitHub Actions authenticates with AWS using OIDC (OpenID Connect), eliminating the need for long-lived access keys. The role follows the principle of least privilege and grants only the permissions required for ECR operations and S3 access.

### Kubernetes Cluster (kind)

The cluster is provisioned locally using kind (Kubernetes in Docker) and managed through Terraform. It consists of one control-plane node and two worker nodes, providing a realistic multi-node setup for testing high availability and workload distribution.

---

## CI/CD Pipeline

### CI Pipeline (Pull Requests)

Triggered on every pull request targeting `main`. Runs security scans with Trivy against the filesystem and Docker images, and validates that all services build successfully without pushing to the registry.

### CD Pipeline (Merge to main)

Triggered on every merge to `main`. Builds Docker images for all three services, pushes them to ECR tagged with the Git commit SHA, and updates the image tag reference in the repository. ArgoCD detects the change and automatically deploys to the cluster.

```
PR opened
    |
CI Pipeline runs (tests + security scan)
    |
Code review and approval
    |
Merge to main
    |
CD Pipeline runs (build + push to ECR)
    |
ArgoCD detects Git change
    |
Automatic deployment to cluster
```

---

## Monitoring

### Prometheus

Collects metrics from all cluster components including nodes, pods, and Kubernetes system components. Configured with a 7-day retention period.

### Grafana

Visualizes metrics from Prometheus. Pre-configured with dashboards for cluster resource usage, node health, networking, and workload performance. Admin credentials are managed as Kubernetes secrets.

### AlertManager

Handles alert routing and deduplication. Integrates with Prometheus alerting rules to notify on critical cluster events.

### Loki + Promtail

Loki aggregates logs from all pods across the cluster. Promtail runs as a DaemonSet, ensuring one log collector per node so no logs are missed. Logs are queryable directly from Grafana alongside metrics.

---

## GitOps with ArgoCD

ArgoCD continuously monitors the Git repository and reconciles the cluster state to match what is defined in Git. Any manual change made directly to the cluster will be automatically reverted to match the Git state.

Applications are configured with automatic sync enabled. Rollback to any previous deployment is available through the ArgoCD UI by selecting a previous Git revision.

---

## Auto Scaling

Horizontal Pod Autoscaler (HPA) is configured for the demo workload with a CPU target of 50%. The minimum replica count is 2 and the maximum is 4. When load increases beyond the threshold, Kubernetes automatically schedules additional pods. When load decreases, pods are scaled back down after a cooldown period.

This was validated with k6 load testing, which demonstrated the full scale-up and scale-down cycle visible in Grafana dashboards.

---

## Load Testing

k6 load tests simulate realistic traffic patterns against the cluster. The test script uses a staged approach: ramping up to 20 virtual users over 30 seconds, sustaining 50 virtual users for 1 minute, then ramping down. This is sufficient to trigger HPA scaling events and validate cluster behavior under load.

---

## CronJobs

A Kubernetes CronJob runs on a scheduled interval to simulate operational tasks such as cleanup, reporting, or health verification. The job runs an Alpine container, executes the task, and terminates cleanly. Kubernetes retains job history for log inspection.

---

## Local Development

### Prerequisites

- WSL2 with Ubuntu 24.04
- Docker Desktop with WSL2 integration enabled
- kubectl, kind, terraform, helm, aws cli, git, k6, ngrok

### Access Services Locally

```bash
# Start port-forwarding for monitoring tools
bash scripts/start-services.sh

# Grafana
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring

# Prometheus
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring

# ArgoCD
kubectl port-forward svc/argocd-server 8080:443 -n argocd
```

### Run Load Test

```bash
kubectl port-forward svc/podinfo 9898:9898 -n podinfo &
k6 run k6/load-test.js
```

---

## Key Concepts Demonstrated

This project covers the following areas relevant to Infrastructure and DevOps engineering roles.

Infrastructure as Code using Terraform with a modular structure supporting multiple environments. Kubernetes cluster management including deployments, services, ingress, autoscaling, and scheduled jobs. Container lifecycle management from build through registry to deployment. GitOps principles using ArgoCD where Git is the single source of truth for cluster state. Observability through metrics collection, log aggregation, and dashboard visualization. Secure cloud authentication using OIDC without static credentials. Automated CI/CD pipelines that enforce code review and testing before deployment.

---

## Author

Ermal Shala

---

## Security Notice

Before deploying this platform, replace all placeholder values:

- `kubernetes/monitoring/values.yaml` — replace `adminPassword` with a strong password
- `kubernetes/monitoring/values.yaml` — replace `slack_api_url` with your own Slack webhook URL
- Never commit real credentials to version control

## Contributing

This is a personal learning project. Feel free to fork and adapt it for your own use.

## License


---

## Quick Recovery (Monitoring Stack)

Nëse cluster-i riniset dhe duhet të rikonfigurosh monitoring:

### 1. Prometheus + Grafana
```bash
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --values kubernetes/monitoring/values.yaml
```

### 2. Loki
```bash
helm upgrade --install loki grafana/loki \
  --namespace monitoring \
  --values kubernetes/loki/values.yaml
```

### 3. Promtail
```bash
helm upgrade --install promtail grafana/promtail \
  --namespace monitoring \
  --values kubernetes/promtail/values.yaml
```

### 4. Loki datasource ne Grafana
```bash
kubectl exec -n monitoring deploy/prometheus-grafana -c grafana -- \
  curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Loki","type":"loki","url":"http://loki-gateway.monitoring.svc.cluster.local","access":"proxy","isDefault":false}' \
  "http://admin:devops123@localhost:3000/api/datasources"
```

### 5. Access tools
```bash
# Grafana
kubectl port-forward -n monitoring deploy/prometheus-grafana 3000:3000

# ArgoCD
kubectl port-forward svc/argocd-server 8080:443 -n argocd

# Pastaj ngrok per akses extern
ngrok http 3000

