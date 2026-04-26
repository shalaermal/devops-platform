output "s3_bucket_name" {
  description = "Name of S3 bucket"
  value       = module.s3.bucket_name
}

output "ecr_repository_urls" {
  description = "URLs e ECR repositories"
  value       = module.ecr.repository_urls
}

output "github_actions_role_arn" {
  description = "ARN of GitHub Actions role"
  value       = module.iam.github_actions_role_arn
}