#!/bin/bash
set -e

echo "==> Starting monitoring stack..."

helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --values kubernetes/monitoring/values.yaml

helm upgrade --install loki grafana/loki \
  --namespace monitoring \
  --values kubernetes/loki/values.yaml

helm upgrade --install promtail grafana/promtail \
  --namespace monitoring \
  --values kubernetes/promtail/values.yaml

echo "==> Waiting for Grafana to be ready..."
kubectl rollout status deployment/prometheus-grafana -n monitoring --timeout=120s

echo "==> Adding Loki datasource..."
kubectl exec -n monitoring deploy/prometheus-grafana -c grafana -- \
  curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Loki","type":"loki","url":"http://loki-gateway.monitoring.svc.cluster.local","access":"proxy","isDefault":false}' \
  "http://admin:devops123@localhost:3000/api/datasources" || true

echo "==> Starting port-forwards..."
kubectl port-forward -n monitoring deploy/prometheus-grafana 3000:3000 &
kubectl port-forward svc/argocd-server 8080:443 -n argocd &

echo ""
echo "Done! Platform is ready."
echo "Grafana:  http://localhost:3000  (admin/devops123)"
echo "ArgoCD:   http://localhost:8080"
echo "Run 'ngrok http 3000' for external access."
