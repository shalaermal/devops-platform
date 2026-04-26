output "cluster_name" {
  description = "Emri i clusterit"
  value       = kind_cluster.this.name
}

output "kubeconfig" {
  description = "Kubeconfig për të aksesuar clusterin"
  value       = kind_cluster.this.kubeconfig
  sensitive   = true
}