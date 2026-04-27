#!/bin/bash

pkill -f "kubectl port-forward" 2>/dev/null

while true; do kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring --address 0.0.0.0 2>/dev/null; sleep 2; done &

while true; do kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring --address 0.0.0.0 2>/dev/null; sleep 2; done &

echo "Grafana: http://localhost:3000"
echo "Prometheus: http://localhost:9090"