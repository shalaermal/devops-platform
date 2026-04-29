# Alerting Runbook

## PodCrashLooping
**Symptom:** Pod restarts repeatedly  
**Check:** `kubectl logs <pod> -n <namespace>`  
**Fix:** Check resource limits, image errors, config issues

## HighCPUUsage
**Symptom:** CPU > 80% for 2+ minutes  
**Check:** `kubectl top pods -n <namespace>`  
**Fix:** Scale deployment or optimize application

## PodNotReady
**Symptom:** Pod not ready for 2+ minutes  
**Check:** `kubectl describe pod <pod> -n <namespace>`  
**Fix:** Check readiness probe, dependencies, network
