output "repository_urls" {
  description = "URLs e ECR repositories"
  value = {
    for name in var.repository_names :
    name => aws_ecr_repository.this[name].repository_url
  }
}