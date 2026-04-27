# Grafana
while true; do kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring --address 0.0.0.0 2>/dev/null; sleep 2; done &

# Prometheus
while true; do kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring --address 0.0.0.0 2>/dev/null; sleep 2; done &


Grafana    → http://localhost:3000  (admin/devops123)
Prometheus → http://localhost:9090