variable "environment" {
  description = "Environment (dev, prod)"
  type        = string
}

variable "github_org" {
  description = "GitHub organization or username"
  type        = string
}

variable "github_repo" {
  description = "Emri i GitHub repository"
  type        = string
}

variable "ecr_repository_arns" {
  description = "ARN-et e ECR repositories"
  type        = list(string)
}

variable "s3_bucket_arn" {
  description = "ARN i S3 bucket"
  type        = string
}